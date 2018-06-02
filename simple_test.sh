#!/bin/sh

# Input
echo """Transaction ID	Market	Type	Price	Amount	Fee	Gas Fee	Total	Date	Status
XCXCXCXC-5c40-11e8-8e87-0be4c258aaef	UBT/ETH	Sell	0.00018904	1 UBT	0.1 ETH	undefined ETH	0.5 ETH	2018-01-20 13:00:00	COMPLETE
XCXCXCXC-5c24-11e8-8e87-0be4c258aaef	UBT/ETH	Buy	0.00011515	1 UBT	0.1 UBT	N/A	0.5 ETH	2018-01-20 12:00:00	COMPLETE""" > tmp_test_input.csv

# Test mit Abziehen der Fees
echo """Type,Buy,CurB,Sell,CurS,Fee,CurF,Exchange,Group,Comment,Trade ID,Date
Trade,0.4,ETH,1,UBT,0.1,ETH,Idex,,,XCXCXCXC-5c40-11e8-8e87-0be4c258aaef,2018-01-20 13:00:00
Trade,0.9,UBT,0.5,ETH,0.1,UBT,Idex,,,XCXCXCXC-5c24-11e8-8e87-0be4c258aaef,2018-01-20 12:00:00""" > tmp_test_output_soll.csv

./idex2ct.py tmp_test_input.csv Y

diff -w tmp_test_input_UploadCT.csv tmp_test_output_soll.csv
if [[ $? -ne 0 ]]
then
  echo "Test mit Abziehen der Fees: FEHLER!!!!!"
  exit 0
else
  echo "Test mit Abziehen der Fees: OK"
fi

./idex2ct.py tmp_test_input.csv

diff -w tmp_test_input_UploadCT.csv tmp_test_output_soll.csv
if [[ $? -ne 0 ]]
then
  echo "Test mit Abziehen der Fees (Default): FEHLER!!!!!"
  exit 0
else
  echo "Test mit Abziehen der Fees (Default): OK"
fi


# Test OHNE Abziehen der Fees
echo """Type,Buy,CurB,Sell,CurS,Fee,CurF,Exchange,Group,Comment,Trade ID,Date
Trade,0.5,ETH,1,UBT,0.1,ETH,Idex,,,XCXCXCXC-5c40-11e8-8e87-0be4c258aaef,2018-01-20 13:00:00
Trade,1,UBT,0.5,ETH,0.1,UBT,Idex,,,XCXCXCXC-5c24-11e8-8e87-0be4c258aaef,2018-01-20 12:00:00""" > tmp_test_output_soll.csv

./idex2ct.py tmp_test_input.csv N

diff -w tmp_test_input_UploadCT.csv tmp_test_output_soll.csv
if [[ $? -ne 0 ]]
then
  echo "Test mit Abziehen der Fees: FEHLER!!!!!"
  exit 0
else
  echo "Test mit Abziehen der Fees: OK"
fi

# Aufrauemen
rm -f tmp_test_output_soll.csv tmp_test_input_UploadCT.csv tmp_test_input.csv
