# Starting String
string_start = "Reference_Pool_ID VARCHAR(4), Loan_Identifier VARCHAR(12), Monthly_Reporting_Period DATE, Channel VARCHAR(1), Seller_Name VARCHAR(50), Servicer_Name VARCHAR(50), Master_Servicer VARCHAR(10), Original_Interest_Rate NUMERIC(5,3), Current_Interest_Rate NUMERIC(5,3), Original_UPB NUMERIC(12,2), UPB_at_Issuance NUMERIC(12,2), Current_Actual_UPB NUMERIC(12,2), Original_Loan_Term INTEGER, Origination_Date DATE, First_Payment_Date DATE, Loan_Age INTEGER, Remaining_Months_to_Legal_Maturity INTEGER, Maturity_Date DATE, Original_Loan_to_Value_Ratio_LTV NUMERIC(3), Original_Combined_Loan_to_Value_Ratio_CLTV NUMERIC(3), Number_of_Borrowers INTEGER, Debt_To_Income_DTI NUMERIC(3), Borrower_Credit_Score_at_Origination INTEGER, Co_Borrower_Credit_Score_at_Origination INTEGER, First_Time_Home_Buyer_Indicator VARCHAR(1), Loan_Purpose VARCHAR(1), Property_Type VARCHAR(2), Number_of_Units INTEGER, Occupancy_Status VARCHAR(1), Property_State VARCHAR(2), Metropolitan_Statistical_Area_MSA INTEGER, Zip_Code_Short VARCHAR(3), Mortgage_Insurance_Percentage NUMERIC(5,2), Amortization_Type VARCHAR(3), Prepayment_Penalty_Indicator VARCHAR(1), Interest_Only_Loan_Indicator VARCHAR(1), Interest_Only_First_Principal_And_Interest_Payment_Date DATE, Months_to_Amortization INTEGER, Current_Loan_Delinquency_Status VARCHAR(2), Loan_Payment_History VARCHAR(48), Modification_Flag VARCHAR(1), Mortgage_Insurance_Cancellation_Indicator VARCHAR(2), Zero_Balance_Code VARCHAR(3), Zero_Balance_Effective_Date DATE, UPB_at_the_Time_of_Removal NUMERIC(12,2), Repurchase_Date DATE, Scheduled_Principal_Current NUMERIC(12,2), Total_Principal_Current NUMERIC(12,2), Unscheduled_Principal_Current NUMERIC(12,2), Last_Paid_Installment_Date DATE, Foreclosure_Date DATE, Disposition_Date DATE, Foreclosure_Costs NUMERIC(12,2), Property_Preservation_and_Repair_Costs NUMERIC(12,2), Asset_Recovery_Costs NUMERIC(12,2), Miscellaneous_Holding_Expenses_and_Credits NUMERIC(12,2), Associated_Taxes_for_Holding_Property NUMERIC(12,2), Net_Sales_Proceeds NUMERIC(12,2), Credit_Enhancement_Proceeds NUMERIC(12,2), Repurchase_Make_Whole_Proceeds NUMERIC(12,2), Other_Foreclosure_Proceeds NUMERIC(12,2), Modification_Related_Non_Interest_Bearing_UPB NUMERIC(12,2), Principal_Forgiveness_Amount NUMERIC(12,2), Original_List_Start_Date DATE, Original_List_Price NUMERIC(12,2), Current_List_Start_Date DATE, Current_List_Price NUMERIC(12,2), Borrower_Credit_Score_At_Issuance INTEGER, Co_Borrower_Credit_Score_At_Issuance INTEGER, Borrower_Credit_Score_Current INTEGER, Co_Borrower_Credit_Score_Current INTEGER, Mortgage_Insurance_Type VARCHAR(1), Servicing_Activity_Indicator VARCHAR(1), Current_Period_Modification_Loss_Amount NUMERIC(12,2), Cumulative_Modification_Loss_Amount NUMERIC(12,2), Current_Period_Credit_Event_Net_Gain_or_Loss NUMERIC(12,2), Cumulative_Credit_Event_Net_Gain_or_Loss NUMERIC(12,2), Special_Eligibility_Program VARCHAR(1), Foreclosure_Principal_Write_off_Amount NUMERIC(12,2), Relocation_Mortgage_Indicator VARCHAR(1), Zero_Balance_Code_Change_Date DATE, Loan_Holdback_Indicator VARCHAR(1), Loan_Holdback_Effective_Date DATE, Delinquent_Accrued_Interest NUMERIC(12,2), Property_Valuation_Method VARCHAR(1), High_Balance_Loan_Indicator VARCHAR(1), ARM_Initial_Fixed_Rate_Period_5YR_or_Less_Indicator VARCHAR(1), ARM_Product_Type VARCHAR(100), Initial_Fixed_Rate_Period INTEGER, Interest_Rate_Adjustment_Frequency INTEGER, Next_Interest_Rate_Adjustment_Date DATE, Next_Payment_Change_Date DATE, Loan_Index VARCHAR(100), ARM_Cap_Structure VARCHAR(10), Initial_Interest_Rate_Cap_Up_Percent NUMERIC(6,4), Periodic_Interest_Rate_Cap_Up_Percent NUMERIC(6,4), Lifetime_Interest_Rate_Cap_Up_Percent NUMERIC(6,4), Mortgage_Margin NUMERIC(6,4), ARM_Balloon_Indicator VARCHAR(1), ARM_Plan_Number INTEGER, Borrower_Assistance_Plan VARCHAR(1), High_Loan_to_Value_HLTV_Refinance_Option_Indicator VARCHAR(1), Deal_Name VARCHAR(200), Repurchase_Make_Whole_Proceeds_Flag VARCHAR(1), Alternative_Delinquency_Resolution VARCHAR(1), Alternative_Delinquency_Resolution_Count INTEGER, Total_Deferral_Amount NUMERIC(12,2), Payment_Deferral_Modification_Event_Indicator VARCHAR(1), Interest_Bearing_UPB NUMERIC(12,2)"

# Split string on ', '
string_list = string_start.split(sep=', ')

# Iterate through list and split into key value pairs on ' '
schema_dict = {}
for item in string_list:
    key, value = item.split(sep=' ')
    schema_dict[key] = value

date_columns = []

date_dict = {}

# Iterate through schema_dict and note all that have value of "DATE"
i = -1 # Start before the first column to account for zero-indexing
for key, value in schema_dict.items():
    i += 1
    if value == 'DATE':
        date_columns.append(i)
        date_dict[key] = value

print(date_columns)
print(date_dict)