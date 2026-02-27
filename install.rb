#!/usr/bin/env ruby
# Moony Ruby-style installer (self-contained)

# Function to check if a command exists
def command_exists?(cmd)
  system("which #{cmd} > /dev/null 2>&1")
end

# Install Ruby if missing
unless command_exists?("ruby")
  puts "[*] Ruby not found. Installing Ruby..."
  system("pkg update -y")
  system("pkg upgrade -y")
  system("pkg install ruby -y")
else
  puts "[*] Ruby is already installed."
end

# Ensure Python & pip are installed
unless command_exists?("python")
  puts "[*] Python not found. Installing Python..."
  system("pkg install python -y")
end

puts "[*] Ensuring pip is installed & up-to-date..."
system("python -m ensurepip")
system("pip install --upgrade pip")

# Install Python dependencies
puts "[*] Installing Python dependencies for Moony..."
packages = [
  "requests>=2.31.0",
  "beautifulsoup4>=4.12.2",
  "dnspython>=2.4.2",
  "python-whois>=0.8.0",
  "colorama>=0.4.6",
  "tldextract>=5.1.1",
  "urllib3>=2.0.7"
]

packages.each do |pkg|
  puts "[*] Installing #{pkg}..."
  system("pip install #{pkg}")
end

puts "[✔] Moony setup complete!"
