# import json
# from pathlib import Path

# # Load the original ARM template file
# # file_path = "/mnt/data/ARMTemplateForFactory.json"
# file_path = "/mnt/c/Users/LILTIMZ/Desktop/ARMTemplateForFactory.json"
# with open(file_path, "r", encoding="utf-8") as file:
#     arm_data = json.load(file)

# Define the dataset/pipeline names we want to include (keywords from user's list)
import json
from pathlib import Path

# Define paths
input_path = Path("/mnt/c/Users/LILTIMZ/Desktop/ARMTemplateForFactory.json")
output_path = Path("/mnt/c/Users/LILTIMZ/Desktop/Filtered_ARMTemplate.json")

keywords = [
    "ACC_RNT_LWORK_DAY", "Account_balance", "D_F_ACCT_ENT_LWORK_DAY", "FBNK_RE_STAT_LINE_CONT_SOURCE",
    "Joint_contracts", "SOURCE_ACCOUNT", "SOURCE_ACCOUNT2", "SOURCE_ACCOUNT3", "SOURCE_ACCOUNT4",
    "SOURCE_ACCOUNT5", "SOURCE_ACCOUNT_BALANCE_2", "SOURCE_ACCOUNT_CLOSED", "SOURCE_ACCOUNT_CLOSURE",
    "SOURCE_ACCOUNT_CREDIT_INT", "SOURCE_ACCOUNT_DEBIT_INT", "SOURCE_ACCOUNT_OVERDRAWN",
    "SOURCE_ACCOUNT_PAT", "SOURCE_ACCT_INACTIVE_RESET", "SOURCE_AC_LOCKED_EVENT", "SOURCE_CARD_ISSUE",
    "SOURCE_CARD_STATUS", "SOURCE_CARD_TYPE", "SOURCE_CATEGORY", "SOURCE_CATEG_ENTRY", "SOURCE_COLLATERAL",
    "SOURCE_COLLATERAL_TYPE", "SOURCE_COMPANY", "SOURCE_CURRENCY", "SOURCE_CUSTOMER", "SOURCE_CUSTOMER_2",
    "SOURCE_DEPT_ACCT_OFFICER", "SOURCE_FUNDS_TRANSFER", "SOURCE_F_EB_PHB_PRODUCT_TYPE",
    "SOURCE_F_MB_TXN_ENTRY_PARAM", "SOURCE_GROUP_CREDIT_INT", "SOURCE_GROUP_DEBIT_INT",
    "SOURCE_LETTER_OF_CREDIT", "SOURCE_LIMIT", "SOURCE_LMM_CUSTOMER", "SOURCE_MM_MONEY_MARKET",
    "SOURCE_PD_BALANCES", "SOURCE_PD_PAYMENT_DUE", "SOURCE_PRODUCT", "SOURCE_SECTOR",
    "SOURCE_SECURITY_POSITION", "SOURCE_STMT_ENTRY", "SOURCE_STMT_ENTRY1", "SOURCE_T24_DATE",
    "SOURCE_TRANSACTION", "SRC_STMT_ENTRY", "STMNT_ENTRY_PARA", "Source_T24_Funds_Transfer",
    "Source_T24_Funds_Transfer_new", "Source_account_balance", "Source_daocode", "Source_fx",
    "Source_user_inputter", "T24DB_SOURCE_ACOOUNT", "colateral_right", "ld_loans_and_deposits",
    "lmm_acc_bal", "mc_register_so", "source_cad_bond", "source_cad_loan", "source_cad_mortgage",
    "source_f_local_ref", "source_f_local_table", "source_forex", "source_industry",
    "source_ld_loan_schedule", "source_sec_acc_mastr", "source_standard_selection", "source_teller",
    "src_cust_document", "src_trans_document"
]

# # Always keep parameters and variables from the original
# filtered_template = {
#     "$schema": arm_data["$schema"],
#     "contentVersion": arm_data["contentVersion"],
#     "parameters": arm_data["parameters"],
#     "variables": arm_data["variables"],
#     "resources": []
# }

# # Filter resources based on keyword match in name
# for resource in arm_data["resources"]:
#     name = resource.get("name", "").lower()
#     if any(keyword.lower() in name for keyword in keywords):
#         filtered_template["resources"].append(resource)

# # Save the filtered ARM template
# filtered_path = "/mnt/c/Users/LILTIMZ/Desktop/ARMTemplateForFactory.json"
# with open(filtered_path, "w", encoding="utf-8") as f:
#     json.dump(filtered_template, f, indent=4)

# filtered_path


try:
    # Load the original ARM template
    with open(input_path, "r", encoding="utf-8") as file:
        arm_data = json.load(file)

    # Filter logic
    filtered_template = {
        "$schema": arm_data["$schema"],
        "contentVersion": arm_data["contentVersion"],
        "parameters": arm_data["parameters"],
        "variables": arm_data["variables"],
        "resources": [
            resource for resource in arm_data["resources"]
            if any(keyword.lower() in resource.get("name", "").lower() for keyword in keywords)
        ]
    }

    # Save the filtered template
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_template, f, indent=4)

    print(f"✅ Filtered ARM template saved to: {output_path}")

except FileNotFoundError:
    print(f"❌ Error: File not found at {input_path}")
except json.JSONDecodeError:
    print(f"❌ Error: Invalid JSON in {input_path}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
