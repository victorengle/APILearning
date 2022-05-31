from app.random_calculations import BankAccount, add, substract, multiply, divide, InsufficientFunds
import pytest


@pytest.mark.parametrize("num1, num2, result", [(3, 6, 9), (5, 2, 7), (9, 4, 13)])
def test_add(num1, num2, result):
    print("Testing Function")
    sum_test = add(num1, num2)
    assert sum_test == result


def test_subtract():
    print("Testing Function")
    sum_test = substract(5, 3)
    assert sum_test == 2


def test_multiply():
    print("Testing Function")
    sum_test = multiply(5, 3)
    assert sum_test == 15


def test_divide():
    print("Testing Function")
    sum_test = divide(6, 3)
    assert sum_test == 2


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    zero_bank_account = BankAccount()
    print("testing my bank account")
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposit, withdraw, result", [(500, 150, 350), (50, 10, 40), (1000, 400, 600)])
def test_bank_transactions(zero_bank_account, deposit, withdraw, result):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == result


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
