# 🔐 Password-Analyzer-Wordlist-Generator-Tool

A Python-based GUI application that helps analyze password strength and generate a custom wordlist based on user inputs. Ideal for security enthusiasts and penetration testers to quickly create targeted wordlists.

## 🚀 Features
- Password strength analysis using `zxcvbn`
- Generate wordlist with name, DOB, and pet name mutations
- Leetspeak and year-based variants included
- Save generated wordlist to a file
- Light and Dark mode themes
- Adjustable font size

## ⚙️ Installation
1. Clone the repository:  
   `git clone https://github.com/your-username/password-tool.git`
2. Install dependencies:  
   - Windows --> `pip install zxcvbn tkinter`
   - Linux   --> `apt install python3-zxcvbn && apt install python3-tkinter`

## 🧱 Usage
Run the tool by executing:  
`python password_&_wordlist_tool.py`

1. Enter a password to analyze.  
2. Optionally provide name, date of birth, and pet name.  
3. Click "Analyze & Generate Wordlist".  
4. Preview results in the output box.  
5. Select save location and click "💾 Save Wordlist" to export.

## 🖼️ Sample Screenshots
**Main GUI Interface**
![Main Interface](images/main_interface.png) 

**Wordlist Generated Example**  
![Wordlist Output](images/wordlist_output.png)

## 🎯 Example Use Cases
- Generate targeted wordlists for penetration tests  
- Evaluate password strength and get actionable feedback  
- Save wordlist for brute force attacks or dictionary attacks  

## 📚 Technical Details
- Leetspeak substitutions: e.g., 'a' → '@', '4'  
- Append years (1990–2030) to words  
- `zxcvbn` library used for password strength estimation  
- Tkinter GUI for easy interaction  

## ⚠️ Disclaimer
This tool is intended for educational purposes and authorized security assessments only. Unauthorized use may be illegal.
