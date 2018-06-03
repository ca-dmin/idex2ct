#!/usr/bin/python
# coding=utf-8

import csv
import sys

# bei True: Gebuhren (Fee + GasFee) von dem Buy-Wert anziehen
# bei False: nix tun
flagFeesAbziehen = True

if len(sys.argv) == 1:
    print("Fehler! Bitte Dateiname uebergeben!")
    print("")
    print("Usage: idex2ct.py <inputFile> [Y/N = Fees Abziehen vom Buy-Betrag; Default Y]  ")
    print("")
    print("OutputFile ist <inputFile>._UploadCT.csv")
    print("")
    exit()


inputFilename = sys.argv[1]
outputFilename = str(inputFilename.split('.')[0]) + "_UploadCT.csv"

if (len(sys.argv) > 2) and (sys.argv[2] == "N"):
    flagFeesAbziehen = False

with open(outputFilename, 'w') as csvfile:
    fieldnames = ['Type', 'Buy', 'CurB', 'Sell', 'CurS', 'Fee', 'CurF', 'Exchange', 'Group', 'Comment', 'Trade ID', 'Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\r\n')
    writer.writeheader()
    with open(inputFilename, 'r') as csvfile:
        inputReader = csv.DictReader(csvfile, delimiter='\t')
        for row in inputReader:
            # Defaults
            Type='Trade'
            Buy=''
            CurB=''
            Sell=''
            CurS=''
            if (row['Type'] == 'Buy'):
                  [Buy, CurB] = row['Amount'].split(' ');
                  [Sell, CurS] = row['Total'].split(' ')
            elif (row['Type'] == 'Sell'):
                  [Sell, CurS] = row['Amount'].split(' ');
                  [Buy, CurB] = row['Total'].split(' ')
            # Fee
            Fee = 0.0
            GFee = 0.0
            try:
                CurF = row['Fee'].split(' ')[1]
                Fee = float(row['Fee'].split(' ')[0])
            except ValueError as e:
                Fee = 0.0
                #print(e.message)

            try:
                GFee = float(row['Gas Fee'].split(' ')[0])
            except ValueError as e:
                GFee = 0.0
                #print(e.message)
            # Fee = Fee + Gas Fee
            Fee += float(GFee)

            # Fees abziehen?
            if flagFeesAbziehen:
                Buy = float(Buy) - Fee
            if CurF != CurB:
                print("FEHLER!?!?! CurF != CurB?")

            Exchange='Idex'
            Group=''
            Comment=''
            TradeID=row['Transaction ID']
            Date=row['Date']

            writer.writerow({
            'Type': Type
            , 'Buy': Buy
            , 'CurB': CurB
            , 'Sell': Sell
            , 'CurS': CurS
            , 'Fee': Fee
            , 'CurF': CurF
            , 'Exchange': Exchange
            , 'Group': Group
            , 'Comment': Comment
            , 'Trade ID': TradeID
            , 'Date': Date })

print("Done: " + inputFilename + " --> " + outputFilename + " erstellt.")
