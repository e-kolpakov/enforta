from collections import defaultdict
from DocApprovalNotifications.notification_strategies.cleanup import CleanAllApproversStrategy
from DocApprovalNotifications.notification_strategies.immediate import NotifyCreatorStrategy


class NotificationStrategiesRepository(object):
    _instance = None

    def __init__(self):
        self.repository = defaultdict(list)

    def __getitem__(self, item):
        return self.repository[item]

    def register_strategy(self, event_type, notifier):
        self.repository[event_type].append(notifier)

    def register_strategies(self):
        from DocApprovalNotifications.notification_strategies.immediate import NotifyApproversInNextStepStrategy
        from DocApprovalNotifications.models import Event

        self.register_strategy(Event.EventType.REQUEST_APPROVAL_STARTED, NotifyApproversInNextStepStrategy)
        self.register_strategy(Event.EventType.REQUEST_APPROVAL_CANCELLED, CleanAllApproversStrategy)

        self.register_strategy(Event.EventType.REQUEST_APPROVED, NotifyApproversInNextStepStrategy)
        self.register_strategy(Event.EventType.REQUEST_APPROVED, NotifyCreatorStrategy)
        # self.register_strategy(Event.EventType.REQUEST_APPROVED, RecurringNotificationApproversInNextStepStrategy)
        # self.register_strategy(Event.EventType.REQUEST_APPROVED, CleanApproversInCurrentStepStrategy)

        self.register_strategy(Event.EventType.REQUEST_REJECTED, NotifyCreatorStrategy)
        self.register_strategy(Event.EventType.REQUEST_REJECTED, CleanAllApproversStrategy)

        self.register_strategy(Event.EventType.REQUEST_FINAL_APPROVE, NotifyCreatorStrategy)
        # self.register_strategy(Event.EventType.REQUEST_FINAL_APPROVE, NotifyAllUsersStrategy)

        # self.register_strategy(Event.EventType.CONTRACT_PAYMENT_REQUIRED, NotifyAccountingStrategy)
        # self.register_strategy(Event.EventType.CONTRACT_PAYMENT_REQUIRED, RecurringNotificationAccountingStrategy)
        # self.register_strategy(Event.EventType.CONTRACT_PAID, CleanAccountingStrategy)

        # self.register_strategy(Event.EventType.CONTRACT_EXPIRED, NotifyAllUsersStrategy)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = NotificationStrategiesRepository()
            cls._instance.register_strategies()
        return cls._instance