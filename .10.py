class ExportProductManager:
    
    def __init__(self):
        
        self.market_database = {
           "885": {"name": "Thailand", "tariff_rate": 0.00},
           "490": {"name": "Japan", "tariff_rate": 0.05},
           "880": {"name": "South Korea", "tariff_rate": 0.06},
           "000": {"name": "USA / Canada", "tariff_rate": 0.08},
           "500": {"name": "United Kingdom", "tariff_rate": 0.07},
        }
       
        self.processed_logs = []
       
    def verify_gs1_checksum(self, barcode):
        """Core Mathematical Logic for EAN-13 Check Digit validation."""
        if len(barcode) != 13 or not barcode.isdigit():
            return False, "Invalid Format"
        
        odds = [int(barcode[i]) for i in range(0, 12, 2)]
        evens = [int(barcode[i]) for i in range(1, 12, 2)]
        total_sum = sum(odds) * 1 + sum(evens) * 3
        
        next_multiple_of_ten = (
            total_sum
            if total_sum % 10 == 0
            else ((total_sum // 10) + 1) * 10
        )
        calculated_digit = next_multiple_of_ten - total_sum
        actual_digit = int(barcode[12])
        
        if calculated_digit == actual_digit:
            return True, "Checksum Passed"
        return False, f"Checksum Failed (Expected: {calculated_digit})"
    
    def evaluate_export_compliance(self, barcode, product_value):
        """Business Intelligence: Evaluates destination tariffs and rules."""
        is_valid, msg = self.verify_gs1_checksum(barcode)
        if not is_valid:
            return {"status": "REJECTED", "reason": msg, "tax_due": 0}
        
        prefix = barcode[0:3]
        market_info = self.market_database.get(
            prefix, {"name": "Unknown Globa Market", "tariff_rate": 0.10}
            )
        
        estimated_tax = product_value * market_info["tariff_rate"]
        
        result = {
            "status": "APPROVED",
            "destination": market_info["name"],
            "tax_due": estimated_tax,
            "reason": "Compliant with GS1 & Tariff standard.",
        }
        
        self.processed_logs.append({"barcode": barcode, "status": result["status"]})
        return result
    
    def display_system_dashboard(self):
        """Prints the analytical summary logs."""
        print(f"\n--- SYSTEM AUDIT LOGS ({len(self.processed_logs)} Items) ---")
        for log in self.processed_logs:
            print(f"Barcode: {log['barcode']} | Status: {log['status']}")
            
if __name__ == "__main__":
    manager = ExportProductManager()
    print("=== WELCOME TO THE INTEGRATED EXPORT COMPLIANCE ENGINE ===")
    
    while True:
        barcode_input = (
            input("\nEnter 13-digit barcode (or type 'exit' to quit): ")
            .strip()
            .lower()
        )
        if barcode_input == "exit":
            break
        
        try:
            value_input = float(input("Enter product commercial value ($): "))
        except ValueError:
            print("X invalid value amount. Skipping...")
            continue
        
        report = manager.evaluate_export_compliance(barcode_input, value_input)
        
        print("\n" + "=" * 45)
        print(f" STATUS: {report['status']}")
        print("=" * 45)
        if report["status"] == "APPROVED":
            print(f" ' Destination : {report['destination']}")
            print(f" ' Est. Tariff : ${report['tax_due']:.2f}")
        print(f" ' Message     : {report['reason']}")
        print("=" * 45)