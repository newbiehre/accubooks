from enum import Enum


class ExpenseCategory(Enum):
    ADVANCE_TAX = "Advance Tax"
    AIR_TRAVEL = "Air Travel Expense"
    AUTOMOBILE = "Automobile Expense"
    EMPLOYEE_ADVANCE = "Employee Advance"
    FUEL_OR_MILEAGE = "Fuel/Mileage Expenses"
    FURNITURE_AND_EQUIPMENT = "Furniture and Equipment"
    IT_AND_INTERNET = "IT and Internet Expenses"
    LODGING = "Lodging"
    MEALS_AND_ENTERTAINMENT = "Meals and Entertainment"
    OFFICE_SUPPLIES = "Office Supplies"
    OTHER = "Other Expenses"
    PARKING = "Parking"
    TELEPHONE_EXPENSE = "Telephone Expense"


class MileageTypeCategory(Enum):
    NON_MILEAGE = "NonMileage"


class PaidThroughCategory(Enum):
    PETTY_CASH = "Petty Cash"
    EMPLOYEE_REIMBURSEMENTS = "Employee Reimbursements"
    CREDIT_CARD = "Credit Card"
