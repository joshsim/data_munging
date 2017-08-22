#! /usr/bin/env python
import pandas as pd
import numpy as np

#In case of encoding issues?
#def changeencode(data, cols):
#    for col in cols:
#        data[col] = data[col].str.decode('iso-8859-1').str.encode('utf-8')
#    return data   

#Read in Data with read_excel... read_csv results in weird encoding issues if touched up in Excel
df_all = pd.read_excel("/Users/joshsim/Desktop/Rcode/details_munged_turk.xlsx")
df_all = df_all.apply(lambda x: x.astype(str).str.lower())
df = df_all[['menu', 'turk1', 'menu_item', 'detail', 'value']]
print(df.head())
print("""Explanation of column values: \n
	menu refers to the filename of the original asset. This should be changed
	to reflect any naming structures we change.\n
	turk1 refers to the first stage of MTurk templates (bounding boxes around
	menu items. These generate the "menu_item" column, but because the enumerated
	"menu_item"s are not keyed to each other, we don't know what menu_item in
	which turk version matches with another, if at all. \n
	menu_item was explained above. It's a unit of information that encapsulates
	a menu item's name, description, and price, if any. \n
	turk2 refers to the second stage of MTurk. Here, we had bounding boxes
	around details, if any. \n
	turk3 refers to the transcription phase \n""")

#Take the mode for each multifactored index aka pick the best name, desc, price per
df_mode = df.groupby(["menu", "turk1", "menu_item", "detail"]).agg(lambda x:x.value_counts().index[0])
#Did unstack create a new pivot_Table with detail as column?
df_mode = df_mode.unstack()
print(df_mode.head())

#Now pivot this table so that hte details are the columns
#df_mode = df_mode.pivot(index="menu", "turk1", "menu_item", columns = "detail", values = "value")
#print(df_mode)

#Getting a count of how often a transcription value was shared by other Turkers. This requires removing turk3 from the index.
#pivot = pd.pivot_table(df, index=["menu", "turk1", "menu_item", "detail", "value"], aggfunc=len)

writer = pd.ExcelWriter('output.xlsx')
df_mode.to_excel(writer)
writer.save()
