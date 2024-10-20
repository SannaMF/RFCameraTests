*** Settings ***
Library     ../Resources/CameraLibrary.py

*** Variables ***


*** Keywords ***
Check is camera started
    ${is_camera_started}=   is camera started
    should be true    ${is_camera_started}

Check is camera stopped
    ${is_camera_stopped}=   is camera started
    should not be true    ${is_camera_stopped}

Check width
    [Arguments]    ${SETWIDTH}
    ${returned_width}=       get camera width
    should be equal    ${SETWIDTH}    ${returned_width}
    log to console    RETURNED WIDTH: ${returned_width}

Check height
    [Arguments]    ${SETHEIGHT}
    ${returned_height}=      get camera height
    should be equal     ${SETHEIGHT}    ${returned_height}
    log to console    RETURNED HEIGHT: ${returned_height}

Check framerate
    [Arguments]     ${SETFRAMERATE}
    ${returned_framerate}=       get camera framerate
    should be equal    ${SETFRAMERATE}      ${returned_framerate}
    log to console    RETURNED FRAMERATE: ${returned_framerate}

Check exposuretime
    [Arguments]    ${SETEXPOSURETIME}
    ${returned_exptime}=     get camera exposuretime
    should be equal    ${SETEXPOSURETIME}   ${returned_exptime}
    log to console    RETURNED EXPTIME: ${returned_exptime}

Check invalid width
    ${returned_width}=      get camera width
    ${default_width}=       convert to number    640
    should be equal    ${default_width}    ${returned_width}
    log to console    RETURNED WIDTH: ${returned_width}

Check invalid height
    ${returned_height}=     get camera height
    ${default_height}=      convert to number    512
    should be equal     ${default_height}    ${returned_height}
    log to console    RETURNED HEIGHT: ${returned_height}
