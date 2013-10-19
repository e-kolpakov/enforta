from collections import defaultdict
from DocApprovalNotifications.notification_strategies.cleanup import *
from DocApprovalNotifications.notification_strategies.immediate import *
from DocApprovalNotifications.notification_strategies.recurring import *


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

        # order is important here - cleanup always BEFORE creating notifications for same strategy
        self.register_strategy(Event.EventType.REQUEST_APPROVAL_STARTED, NotifyApproversInNextStepStrategy)
        self.register_strategy(Event.EventType.REQUEST_APPROVAL_STARTED, RecurringApproversInNextStepStrategy)

        self.register_strategy(Event.EventType.REQUEST_APPROVAL_CANCELLED, CleanAllApproversStrategy)

        self.register_strategy(Event.EventType.REQUEST_APPROVED, CleanApproversInCurrentStepStrategy)
        self.register_strategy(Event.EventType.REQUEST_APPROVED, NotifyApproversInNextStepStrategy)
        self.register_strategy(Event.EventType.REQUEST_APPROVED, NotifyApproverRequestApprovedStrategy)
        self.register_strategy(Event.EventType.REQUEST_APPROVED, RecurringApproversInNextStepStrategy)

        self.register_strategy(Event.EventType.REQUEST_REJECTED, CleanAllApproversStrategy)
        self.register_strategy(Event.EventType.REQUEST_REJECTED, NotifyApproverRequestRejectedStrategy)

        self.register_strategy(Event.EventType.REQUEST_FINAL_APPROVE, NotifyApproverRequestApprovalCompleteStrategy)
        self.register_strategy(Event.EventType.REQUEST_FINAL_APPROVE, NotifyAllUsersFinalApproveStrategy)

        # self.register_strategy(Event.EventType.CONTRACT_PAYMENT_REQUIRED, NotifyAccountingStrategy)
        # self.register_strategy(Event.EventType.CONTRACT_PAYMENT_REQUIRED, RecurringNotificationAccountingStrategy)

        # self.register_strategy(Event.EventType.CONTRACT_PAID, CleanAccountingStrategy)

        self.register_strategy(Event.EventType.CONTRACT_EXPIRED, NotifyAllUsersContractExpiredStrategy)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = NotificationStrategiesRepository()
            cls._instance.register_strategies()
        return cls._instance