def verify_aadhaar(aadhaar_number):
    return len(aadhaar_number) == 12 and aadhaar_number.isdigit()
