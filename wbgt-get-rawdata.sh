yyyymm=$(date +"%Y%m")

# Form the URL based on the current date
url="https://www.wbgt.env.go.jp/est15WG/dl/wbgt_all_$yyyymm.csv"

# Path where you want to save the CSV file
file_path="./data-wbgt/wbgt_raw.csv"

# Download the CSV file using curl
curl -L $url -o $file_path