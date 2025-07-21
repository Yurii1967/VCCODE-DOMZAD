    
      
from pathlib import Path
import re

to_staff_path = Path("Projects/vccode-domzad/staff.txt").absolute()
print(f"Path to staff file: {to_staff_path}")

try:
    text = to_staff_path.read_text(encoding="utf-8")
    print("File content:")
    print(text)
except FileNotFoundError:
    print("❌ File not found.")
    exit()
except PermissionError:
    print("❌ Permission denied.")
    exit()
except Exception as e:
    print(f"❌ Unexpected error while reading the file: {e}")
    exit()


def statement(to_staff_path):
    salaries = []

    try:
        with open(to_staff_path, "r", encoding="utf-8") as f:
            for line in f:
                numbers = re.findall(r'\d+(?:\.\d+)?', line)  # Підтримка десяткових чисел
                salaries.extend(map(float, numbers))

        if not salaries:
            print("⚠️ No salary data found in the file.")
            return

        total_salary = sum(salaries)
        average = total_salary / len(salaries)

        print(f"✅ Total salary is: {total_salary:.2f}, average is: {average:.2f}")

    except FileNotFoundError:
        print("❌ File not found during processing.")
    except ValueError:
        print("❌ Error converting salary to float. Check file formatting.")
    except Exception as e:
        print(f"❌ Unexpected error during processing: {e}")


statement(to_staff_path)
    
        
        
   



  
      
    
      
      
        
        

  


    
    
      
           

