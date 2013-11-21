/*global define*/
define(
    [],
    {
        ActionMessages: {
            confirm_to_negotiation: 'Перевод заявки в состояние "В согласовании" начнет процесс утверждения. Продолжить?',
            confirm_to_project: 'Перевод заявки в состояние "Проект" приведет к остановке текущего процесса утверждения. Продолжить?',
            confirm_approve: "Утвердить заявку?",
            confirm_rejection: "Отклонить заявку?",
            prompt_for_paid_date: "Введите дату оплаты",
            approve_successful: "Заявка утверждена",
            rejection_successful: "Заявка отклонена"
        },

        Common: {
            errors_happened: "Произошли ошибки: ",
            action_successful: "Действие выполнено успешно",
            action_failed: "Не удалось совершить действие: ",
            generic_action_confirmation: "Вы уверены?"
        },

        NotificationMessages : {
            notification_load_failure: "Загрузка оповещений завершилась с ошибкой - оповещения через пользовательский интерфейс недоступны",
            display_title: "Оповещения"
        }
    }
);