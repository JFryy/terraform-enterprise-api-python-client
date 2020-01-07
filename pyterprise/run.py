import requests

class Run(object):

    def __init__(self, run, api_handler):
        self.id = run.id
        self._api_handler = api_handler

        relationships = run.relationships
        self.workspace_id = relationships.workspace.data.id
        self.apply_id = relationships.apply.data.id
        self.configuration_version = relationships.configuration_version.data.id
        self.plan_id = relationships.plan.data.id
        self.run_events = relationships.run_events.data
        self.policy_checks = relationships.policy_checks.data
        self.comments = relationships.comments.data

        attributes = run.attributes
        self.actions = attributes.actions
        self.canceled_at = attributes.canceled_at
        self.created_at = attributes.created_at
        self.has_changes = attributes.has_changes
        self.is_destroy = attributes.is_destroy
        self.message = attributes.message
        self.plan_only = attributes.plan_only
        self.source = attributes.source
        self.status_timestamps = attributes.status_timestamps
        self.status = attributes.status
        self.trigger_reason = attributes.trigger_reason
        self.permissions = attributes.permissions

    def __str__(self):
        return str(self.__dict__)

    def apply(self, comment=None):
        """ Apply a run on instantiate workspace, returns response code. """
        return self._api_handler.call(method='post',
                                      uri=f'runs/{self.id}/actions/apply',
                                      json={'comment': comment})

    def discard(self, comment=None):
        """ Discard a run on instantiate workspace, returns response code. """
        return self._api_handler.call(method='post',
                                      uri=f'runs/{self.id}/actions/discard',
                                      json={'comment': comment})

    def cancel(self, comment=None):
        """ Cancel a run on instantiate workspace, returns response code. """
        return self._api_handler.call(method='post',
                                      uri=f'runs/{self.id}/actions/cancel',
                                      json={'comment': comment})

    def force_cancel(self, comment=None):
        return self._api_handler.call(
            method='post',
            uri=f'runs/{self.id}/actions/force-cancel',
            json={'comment': comment})

    def force_execute(self, comment=None):
        return self._api_handler.call(
            method='post',
            uri=f'runs/{self.id}/actions/force-execute',
            json={'comment': comment})

    def get_plan(self):
        return self._api_handler.call(uri=f'plans/{self.plan_id}').data

    def get_plan_output(self):
        """ Return plan output string of run. """
        plan = self.get_plan()
        return requests.get(plan['attributes']['log-read-url']).content
