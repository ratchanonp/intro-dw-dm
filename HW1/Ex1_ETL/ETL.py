# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd


# %%
data_source_1_path = "./sources/ETLDataSource1.xlsx"
data_source_2_path = "./sources/ETLDataSource2.xlsx"

# %% [markdown]
# # Load Data
# 

# %%
orderSource1 = pd.read_excel(data_source_1_path, sheet_name="orderSource1")
productSource1 = pd.read_excel(data_source_1_path, sheet_name="productSource1")

orderSource2 = pd.read_excel(data_source_2_path, sheet_name="orderSource2")
productSource2 = pd.read_excel(data_source_2_path, sheet_name="productSource2")

stateLookUp = pd.read_excel(data_source_1_path, sheet_name="StateLookup")

# %% [markdown]
# # Transform Source 1
# 

# %%
# Join order and product with OrderID
data_source_1 = pd.merge(orderSource1, productSource1, on="OrderID", how="inner")

# Replace Dictionary
state_dict = dict(zip(stateLookUp["Abbreviation"], stateLookUp["State"]))
data_source_1 = data_source_1.replace({"CustomerState": state_dict})

# Split CustomerName
# Rename CustomerName[0] to CustomerFirstName and CustomerName[0] to CustomerLastName
data_source_1[['CustomerFirstName','CustomerLastName']] = data_source_1["CustomerName"].str.split(" ", n = 1, expand = True)

data_source_1 = data_source_1.drop(columns=["CustomerName"])

# Reorder Attributes alphabetically ascending
data_source_1 = data_source_1.sort_index(axis=1)

# %% [markdown]
# # Transform Source 2
# 

# %%
data_source_2 = pd.merge(orderSource2, productSource2, on="OrderID", how="inner")

# Replace OrderID prefix A with ""
data_source_2["OrderID"] = data_source_2["OrderID"].str.replace("A", "")

# Parse OrderId to int
data_source_2["OrderID"] = data_source_2["OrderID"].astype(int)

# Change CustomerStatus type to nominal
data_source_2["CustomerStatus"] = data_source_2["CustomerStatus"].astype("category")

CustomerStatus_map = {
    0: "Silver",
    1: "Gold",
    2: "Platinum"
}

# Replace CustomerStatus with map
data_source_2["CustomerStatus"] = data_source_2["CustomerStatus"].replace(CustomerStatus_map)

# Remove totalDiscount column
data_source_2 = data_source_2.drop(columns=["TotalDiscount"])

# Generate new column TotalDiscount
data_source_2["TotalDiscount"] = data_source_2["FullPrice"] - data_source_2["ExtendedPrice"]

# Reorder Attributes alphabetically ascending
data_source_2 = data_source_2.sort_index(axis=1)

# %% [markdown]
# # Append and write to Excel
# 

# %%
data_source = pd.concat([data_source_1, data_source_2], ignore_index=True)

# Generate concatenated column customerName from CustomerFirstName and CustomerLastName
data_source["customerName"] = data_source["CustomerFirstName"] + "_" + data_source["CustomerLastName"]

# Remove CustomerFirstName and CustomerLastName
data_source = data_source.drop(columns=["CustomerFirstName", "CustomerLastName"])

# Reorder Attributes alphabetically ascending
data_source = data_source.reindex(sorted(data_source.columns), axis=1)

# Write to Excel
data_source.to_excel("./Result_Python.xlsx", index=False)

data_source


