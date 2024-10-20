*** Settings ***
Documentation    This suite is based on testing the Camera functionality
Library     ../Resources/CameraLibrary.py
Resource    ../Resources/BasicFunctionality.robot

*** Variables ***
${NUM_FRAMES}       5

*** Test Cases ***
Test Camera Framerate minimum value and Exposure time maximum values
    [Documentation]    Test and validate framerate minimum value and exposure time maximum values

    Create Camera

    ${SETFRAMERATE}=    convert to number    1
    Set Camera Framerate        ${SETFRAMERATE}

    ${SETEXPOSURETIME}=     convert to number    30
    ${setexptime}=     Set Camera Exposuretime    ${SETEXPOSURETIME}

    ${SETWIDTH}=    convert to number    600
    Set Camera Width           ${SETWIDTH}

    ${SETHEIGHT}=       convert to number    111
    Set Camera Height    ${SETHEIGHT}

    Camera Start
    Check is camera started

    ${frame}=   Get Camera Frame

    Check framerate         ${SETFRAMERATE}
    Check exposuretime      ${SETEXPOSURETIME}
    Check height    ${SETHEIGHT}
    Check width     ${SETWIDTH}

    Camera Stop
    Check is camera stopped


Test Camera Framerate maximum value and Exposure time minimum values
    [Documentation]    Test and validate framerate maximum value and exposure time minimum values

    Create Camera

    ${SETFRAMERATE}=    convert to number    50.0
    Set Camera Framerate        ${SETFRAMERATE}

    ${SETEXPOSURETIME}=     convert to number    0.1
    ${setexptime}=     Set Camera Exposuretime    ${SETEXPOSURETIME}

    ${SETWIDTH}=    convert to number    260
    Set Camera Width           ${SETWIDTH}

    ${SETHEIGHT}=       convert to number    520
    Set Camera Height    ${SETHEIGHT}

    Camera Start
    Check is camera started

    ${frame}=   Get Camera Frame
    # log to console    Frame: ${frame}

    Check framerate     ${SETFRAMERATE}
    Check exposuretime    ${SETEXPOSURETIME}
    Check height    ${SETHEIGHT}
    Check width     ${SETWIDTH}

    Camera Stop
    Check is camera stopped


Test width and height maximum values
    [Documentation]    Test and validate width and height maximum values

    Create Camera

    ${SETFRAMERATE}=    convert to number    14.0
    Set Camera Framerate        ${SETFRAMERATE}

    ${SETEXPOSURETIME}=     convert to number    6
    ${setexptime}=     Set Camera Exposuretime    ${SETEXPOSURETIME}

    ${SETWIDTH}=    convert to number    1000
    Set Camera Width           ${SETWIDTH}

    ${SETHEIGHT}=       convert to number    1000
    Set Camera Height    ${SETHEIGHT}

    Camera Start
    Check is camera started

    ${frame}=   Get Camera Frame
    # log to console    Frame: ${frame}

    Check framerate     ${SETFRAMERATE}
    Check exposuretime    ${SETEXPOSURETIME}
    Check height    ${SETHEIGHT}
    Check width     ${SETWIDTH}

    Camera Stop
    Check is camera stopped


Test width and height minimum values
    [Documentation]    Test and validate width and height with minimum values

    Create Camera

    ${SETFRAMERATE}=    convert to number    20.0
    Set Camera Framerate        ${SETFRAMERATE}

    ${SETEXPOSURETIME}=     convert to number    19.2
    ${setexptime}=     Set Camera Exposuretime    ${SETEXPOSURETIME}

    ${SETWIDTH}=    convert to number    100
    Set Camera Width           ${SETWIDTH}

    ${SETHEIGHT}=       convert to number    100
    Set Camera Height    ${SETHEIGHT}

    Camera Start
    Check is camera started

    ${frame}=   Get Camera Frame
    # log to console    Frame: ${frame}

    Check framerate     ${SETFRAMERATE}
    Check exposuretime    ${SETEXPOSURETIME}
    Check height    ${SETHEIGHT}
    Check width     ${SETWIDTH}

    Camera Stop
    Check is camera stopped

Test width and height with invalid values
    [Documentation]    Camera returns default values

    Create Camera

    ${SETFRAMERATE}=    convert to number    20.0
    Set Camera Framerate        ${SETFRAMERATE}

    ${SETEXPOSURETIME}=     convert to number    19.2
    ${setexptime}=     Set Camera Exposuretime    ${SETEXPOSURETIME}

    ${SETWIDTH}=    convert to number    90
    Set Camera Width           ${SETWIDTH}

    ${SETHEIGHT}=       convert to number    1001
    Set Camera Height    ${SETHEIGHT}

    Camera Start
    Check is camera started

    ${frame}=   Get Camera Frame
    # log to console    Frame: ${frame}

    Check framerate     ${SETFRAMERATE}
    Check exposuretime    ${SETEXPOSURETIME}
    Check invalid height
    Check invalid width

    Camera Stop
    Check is camera stopped

Test to capture several frames
    [Documentation]    Capture several frames in a loop

    Create Camera

    ${SETFRAMERATE}=    convert to number    20.0
    Set Camera Framerate        ${SETFRAMERATE}

    ${SETEXPOSURETIME}=     convert to number    19.2
    ${setexptime}=     Set Camera Exposuretime    ${SETEXPOSURETIME}

    ${SETWIDTH}=    convert to number    100
    Set Camera Width           ${SETWIDTH}

    ${SETHEIGHT}=       convert to number    100
    Set Camera Height    ${SETHEIGHT}

    Camera Start
    Check is camera started

    FOR     ${index}    IN RANGE    ${NUM_FRAMES}
        ${frame}=   Get Camera Frame
        log to console    Captured Frame: ${index}: ${frame}
    END

    Camera Stop
    Check is camera stopped