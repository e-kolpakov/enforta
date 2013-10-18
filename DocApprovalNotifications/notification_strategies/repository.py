from collections import defaultdict


class NotificationStrategiesRepository(object):
    _instance = None

    def __init__(self):
        self.repository = defaultdict(list)

    def __getitem__(self, item):
        return self.repository[item]

    def register_strategy(self, event_type, notifier):
        self.repository[event_type].append(notifier)

    def register_strategies(self):
        from DocApprovalNotifications.notification_strategies.immediate import NotifyNextApproversStrategy
        from DocApprovalNotifications.models import Event

        self.register_strategy(Event.EventType.REQUEST_APPROVAL_STARTED, NotifyNextApproversStrategy)
        # repository.register_notifier(Event.EventType.REQUEST_APPROVAL_CANCELLED, CleanAllApproversStrategy)
        self.register_strategy(Event.EventType.REQUEST_APPROVED, NotifyNextApproversStrategy)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = NotificationStrategiesRepository()
            cls._instance.register_strategies()
        return cls._instance






        # class EventType:
        #     REQUEST_APPROVAL_STARTED = "REQUEST_APPROVAL_STARTED"
        #     REQUEST_APPROVAL_CANCELLED = "REQUEST_APPROVAL_CANCELLED"
        #     REQUEST_APPROVED = "REQUEST_APPROVED"
        #     REQUEST_REJECTED = "REQUEST_REJECTED"
        #     REQUEST_FINAL_APPROVE = "REQUEST_FINAL_APPROVE"
        #     CONTRACT_PAYMENT_REQUIRED = "CONTRACT_PAYMENT_REQUIRED"
        #     CONTRACT_PAID = "REQUEST_PAID"
        #     CONTRACT_ACTIVATED = "CONTRACT_ACTIVATED"
        #     CONTRACT_EXPIRED = "CONTRACT_EXPIRED"
        #     UNKNOWN = "UNKNOWN"

        # REQUEST_APPROVAL_STARTED - immediate: next approver(s)
        # REQUEST_APPROVAL_CANCELLED - cleanup: all approvers
        # REQUEST_APPROVED -    immediate: next approver(s), creator;
        #                       cleanup: approvers in current step; repeating: next approver(s)
        # REQUEST_REJECTED -    immediate: creator;
        #                       cleanup: approvers in current step
        # REQUEST_FINAL_APPROVE - immediate: creator, all users(?)
        # CONTRACT_PAYMENT_REQUIRED - repeating: accounting
        # CONTRACT_PAID - cleanup: accounting
        # CONTRACT_ACTIVATED - none
        # CONTRACT_EXPIRED - immediate: all users(?)
        # UNKNOWN - none