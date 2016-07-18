# serial_decider.py
import time
import boto.swf.layer2 as swf

class SerialDecider(swf.Decider):

    domain = 'Django_WF_v1'
    task_list = 'default_tasks'
    version = '1.0'

    def run(self):  
        print "Decider is running!"
        history = self.poll()
        print "Polling started."
        if 'events' in history:
            # Get a list of non-decision events to see what event came in last.
            workflow_events = [e for e in history['events']
                               if not e['eventType'].startswith('Decision')]
            decisions = swf.Layer1Decisions()
            # Record latest non-decision event.
            last_event = workflow_events[-1]
            last_event_type = last_event['eventType']
            if last_event_type == 'WorkflowExecutionStarted':
                print "Workflow execution has started!"
                for adi in range(1):
                    print "Decider scheduling task A"
                    decisions.schedule_activity_task('%s-%i' % ('ActivityA', time.time()),
                      'ActivityA', self.version, task_list='a_tasks')
                    #decisions.schedule_activity_task('activity%i' % i, 'ActivityA', '1.0',task_list=self.task_list)
                #print "Decider scheduling task A"
                # Schedule the first activity.
                #decisions.schedule_activity_task('%s-%i' % ('ActivityA', time.time()),
                #  'ActivityA', self.version, task_list='a_tasks')
            elif last_event_type == 'ActivityTaskCompleted':
                print "Decider knows task has finished...it will schedule new task now."
                # Take decision based on the name of activity that has just completed.
                # 1) Get activity's event id.
                last_event_attrs = last_event['activityTaskCompletedEventAttributes']
                completed_activity_id = last_event_attrs['scheduledEventId'] - 1
                # 2) Extract its name.
                activity_data = history['events'][completed_activity_id]
                activity_attrs = activity_data['activityTaskScheduledEventAttributes']
                activity_name = activity_attrs['activityType']['name']
                # 3) Optionally, get the result from the activity.
                result = last_event['activityTaskCompletedEventAttributes'].get('result')

                # Take the decision.
                if activity_name == 'ActivityA':
                    print "Schedule task B"
                    decisions.schedule_activity_task('%s-%i' % ('ActivityB', time.time()),
                        'ActivityB', self.version, task_list='b_tasks', input=result)
                if activity_name == 'ActivityB':
                    print "Schedule task C"
                    decisions.schedule_activity_task('%s-%i' % ('ActivityC', time.time()),
                        'ActivityC', self.version, task_list='c_tasks', input=result)
                elif activity_name == 'ActivityC':
                    print "Execution has completed"
                    # Final activity completed. We're done.
                    decisions.complete_workflow_execution()

            self.complete(decisions=decisions)
            return True