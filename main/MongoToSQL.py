from pymongo import MongoClient


def main():
    client = MongoClient()
    db = client.utilize
    report_table = db.usage_report_table
    reports = report_table.find()

    rows = ["TIMESTAMP,SEL_FULLNESS,FAN1_SPEED,FAN2_SPEED,FAN3_SPEED,FAN4_SPEED,FAN5_SPEED,FAN6_SPEED,PSU1_VOUT,PSU1_IOUT,PSU1_POUT,PSU2_VOUT,PSU2_IOUT,PSU2_POUT,P1_TEMP_SENS,P2_TEMP_SENS,RISER1_INLET_TMP,RISER2_INLET_TMP,RISER1_OUTLETTMP,RISER2_OUTLETTMP,FP_TEMP_SENSOR,DDR3_P1_A1_TEMP,DDR3_P1_A2_TEMP,DDR3_P1_B1_TEMP,DDR3_P1_B2_TEMP,DDR3_P1_C1_TEMP,DDR3_P1_C2_TEMP,DDR3_P1_D1_TEMP,DDR3_P1_D2_TEMP,DDR3_P2_E1_TEMP,DDR3_P2_E2_TEMP,DDR3_P2_F1_TEMP,DDR3_P2_F2_TEMP,DDR3_P2_G1_TEMP,DDR3_P2_G2_TEMP,DDR3_P2_H1_TEMP,DDR3_P2_H2_TEMP,P12V_STBY_V_MOIN,P12V_AUX_V_MOIN,P12V_V_MOIN,P5V_V_MOIN,P3V3_V_MOIN,P1V5_SSB,P1V1_SSB,P3V3_BAT_V_MOIN,PVTT_DDR_AB,PVTT_DDR_CD,PVTT_DDR_EF,PVTT_DDR_GH,PVTT_P1,PVDDQ_AB,PVDDQ_CD,PVSA_P1,PVPLL_P1,PVCCP_P1,PVTT_P2,PVSA_P2,PVCCP_P2,PVDDQ_EF,PVDDQ_GH,PVPLL_P2,POWER_USAGE,P3V3_AUX,P1V8_AUX,P1V5_AUX,P1V0_AUX,P1V1_AUX,P0V75_AUX,PSU1_PIN,PSU2_PIN,PSU1_TEMP,PSU2_TEMP,PCH_TEMP_SENS"]
    for report in reports:
        readings = report['readings']

        row = [str(report['timestamp'])]
        for reading in readings:
            name = reading['name']
            value = reading['value']
            if value is not None and value > 0:
                row.append(str(value))
        rowstring = ",".join(row)
        rows.append(rowstring)

    with open('myfile.csv', 'w') as myfile:
        myfile.write("\n".join(rows))


if __name__ == '__main__':
    main()
