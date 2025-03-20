from aiogram.filters.callback_data import CallbackData


class TariffCallback(CallbackData, prefix="tariff"):
    action: str
    page: int = 0
    tariff_id: int


class PaymentCallback(CallbackData, prefix="payment"):
    action: str
    receipt_id: int


class ConfigCallback(CallbackData, prefix="config"):
    action: str
    page: int = 0
    config_id: int


class ConfigSubCallback(CallbackData, prefix="config_sub"):
    action: str
    page: int = 0
    config_id: int


class ConfigCancelSubCallback(CallbackData, prefix="config_sub_cancel"):
    action: str
    config_id: int


class RetryReccurentCallback(CallbackData, prefix="retry_reccurent"):
    config_id: int

class RestoreSubCallback(CallbackData, prefix="restore_sub"):
    action: str
    config_id: int


class ConfigCancelSubConfirmCallback(CallbackData, prefix="config_sub_cancel_confirm"):
    action: str
    config_id: int


class BalanceCallback(CallbackData, prefix="balance"):
    action: str


class CancelBalanceOperationCallback(CallbackData, prefix="cancel_balance_operation"):
    pass

class CashInMethodCallback(CallbackData, prefix="cash_in_method"):
    method: str


class CashOutMethodCallback(CallbackData, prefix="cash_out_method"):
    method: str


class CompleteCashOutCallback(CallbackData, prefix="complete_cash_out"):
    action: str
    operation_id: int


class OperationCallback(CallbackData, prefix="cashin"):
    action: str
    operation_id: int


class FAQCallback(CallbackData, prefix="faq"):
    action: str


class ThemeCallback(CallbackData, prefix="theme"):
    action: str
    theme_id: int
    page: int = 0


class ProblemCallback(CallbackData, prefix="problem"):
    action: str
    problem_id: int
    theme_id: int
    page: int = 0


class SolutionCallback(CallbackData, prefix="solution"):
    theme_id: int
