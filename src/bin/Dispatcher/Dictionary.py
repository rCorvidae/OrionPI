class DeviceClass:
    PROPULSION = "CPR"
    MANIPULATOR = "CMR"
    CONTAINERS = "CCR"


class SettingsKeys:
    PROPULSION = "PROPULSION"
    MANIPULATOR = "MANIPULATOR"
    CONTAINERS = "CONTAINERS"
    UDP = "UDP"
    TCP_UPDATER_SERVER = "TCP_UPDATER_SERVER"
    UPDATER = "UPDATER"


class PropulsionKeys:
    LEFT_WHEEL_SPEED = "LWS"
    RIGHT_WHEEL_SPEED = "RWS"


class ManipulatorKeysPC:
    TURRET = "TRT"
    SHOULDER_LOWER_ACTUATOR = "SLA"
    ELBOW_UPPER_ACTUATOR = "EUA"
    WRIST_UP_DOWN = "WUD"
    WRIST_ROTATION = "WRN"
    GRIPPER_GEOMETRY = "GGY"
    GRIPPER_GRASPING = "GGG"


class ManipulatorKeysUC:
    TURRET = "TRT"
    SHOULDER_LOWER_ACTUATOR = "SLA"
    ELBOW_UPPER_ACTUATOR = "EUA"
    WRIST_UP_DOWN = "WUD"
    WRIST_ROTATION = "WRN"
    GRIPPER_GEOMETRY = "GGY"
    TOP_FINGER = "TOP_FINGER"
    LEFT_FINGER = "LEFT_FINGER"
    RIGHT_FINGER = "RIGHT_FINGER"
    GRIPPER_GRASPING = {
        TOP_FINGER: "GGGT",
        LEFT_FINGER: "GGGL",
        RIGHT_FINGER: "GGGR"
    }


class ManipulatorDefaultValues:
    TURRET = 0
    SHOULDER_LOWER_ACTUATOR = 0
    ELBOW_UPPER_ACTUATOR = 0
    WRIST_UP_DOWN = 0
    WRIST_ROTATION = 0
    GRIPPER_GEOMETRY = 90
    FINGER_AVERAGE = "FINGER_AVERAGE"
    GRIPPER_GRASPING = {
        ManipulatorKeysUC.TOP_FINGER: 90,
        ManipulatorKeysUC.LEFT_FINGER: 90,
        ManipulatorKeysUC.RIGHT_FINGER: 90,
        FINGER_AVERAGE: 90
    }
