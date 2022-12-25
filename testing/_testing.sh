#!/usr/bin/env false
# This script is sourced from other scripts.

INI_FILE="-c testing/pytest.ini"
REPORT_FOLDER=workspace/testing
REPORT_OPTIONS="--capture=tee-sys --self-contained-html"

mkdir -p ${REPORT_FOLDER}
if [ $? -ne 0 ]; then
    echo -e "\033[1;41m ERROR: COULD NOT CREATE FOLDER ${REPORT_FOLDER} \033[m"
    exit 1
fi

_testing () {
    local test_type="$1"
    local test_type_label="$2"

    REPORT_FILE=${test_type}_$(date +"%FT%H%M%S%z").html
    REPORT_PATH=${REPORT_FOLDER}/${REPORT_FILE}
    REPORT="--html=${REPORT_PATH} ${REPORT_OPTIONS}"

    testing_pass="false"

    if [ "$test_type" == "linting" ]; then
        LINTINGS="--pylint --pylint-rcfile=testing/pylintrc --flake8 --mypy"
        python3 -m pytest ${INI_FILE} -vvv  ${REPORT} --disable-warnings --only-linting ${LINTINGS}
        if [ $? -eq 0 ]; then
            testing_pass="true"
        fi
    fi

    if [ "$test_type" == "modules_test" ]; then
        python3 -m pytest ${INI_FILE} -vvv ${REPORT}
        if [ $? -eq 0 ]; then
            testing_pass="true"
        fi
    fi

    if [ "$testing_pass" == "true" ]; then
        echo -e "\033[1;42m ${test_type_label} PASSED! \033[m"
        exit 0
    fi

    echo -e "\033[1;41m ${test_type_label} FAILED! \033[m"
    wsl_info=$(cat /proc/version)
    if [ $? -eq 0 ]; then
        if [[ "$wsl_info" == *"microsoft-standard-WSL"* ]]; then  # If WSL environment then open test report in Windows
            WINDOWS_REPORT_PATH=$(wslpath -w ${REPORT_PATH})  # <link> https://superuser.com/questions/1113385/convert-windows-path-for-windows-ubuntu-bash
            explorer.exe "${WINDOWS_REPORT_PATH}"  # Open report file with Windows File Explorer
        fi
    fi

    exit 1
}

linting () {
    _testing "linting" "CODE CHECK"
}

module () {
    _testing "modules_test" "MODULE TESTING"
}
