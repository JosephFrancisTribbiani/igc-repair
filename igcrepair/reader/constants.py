from typing import Set


EXTENSION_SUBTYPES: Set[str] = {
    # Linear accelerations in X, Y and Z axes, for aerobatic aircraft equipped with appropriate sensors feeding to
    # the recorder and IGC file. X = longitudinal, Y = lateral, Z = vertical (so-called "G")
    'ACX',
    'ACY',
    'ACZ',
    # Angular accelerations in X, Y and Z axes, for aerobatic aircraft equipped with appropriate sensors feeding to
    # the recorder and IGC file. Pitch = X, roll = Y, yaw = Z in degrees per second
    'ANX',
    'ANY',
    'ANZ',
    # Attitude Pitch Angle, Attitude Bank/Roll Angle in degrees (for nose down or left bank angle, start with "-")
    'AOP',
    'AOR',
    # Altimeter pressure setting in hectoPascals with 4 numbers and one decimal point (for instance, 1013.2, 0995.7).
    # Although an altimeter pressure setting may be recorded (for instance where the FR feeds a cockpit display), it
    # must not be used to change the pressure altitude recorded with each fix, which must remain with respect to the
    # ISA sea level datum of 1013.25 mb at all times
    'ATS',
    # ...
    # The last places of decimal minutes of latitude, where latitude is recorded to a greater precision than the three
    # decimal minutes that are in the main body of the B record. The fourth and any further decimal places of minutes
    # are recorded as an extension to the B record, their position in each B record line being specified in the
    # I record.
    'LAD',
    # Data from the SeeYou system after flight, not needed for Validation but used in some flight analysis systems
    'LCU',
    # The last places of decimal minutes of longitude, where longitude is recorded to a greater precision than the
    # three decimal minutes that are in the main body of the Brecord. The fourth and any further decimal places of
    # minutes are recorded as an extension to the B record, their position in each B record line being specified in
    # the I record.
    'LOD',
}
