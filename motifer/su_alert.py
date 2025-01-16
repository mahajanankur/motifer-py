import logging

# Define a new logging level
SU_ALERT_LEVEL = 35
logging.addLevelName(SU_ALERT_LEVEL, "SUALERT")


# Define the suAlert method for the Logger class
def suAlert(self, message, *args, **kwargs):
    """
    Add a new logging level (SUALERT)
    which will be used as a replacement for GChat Alerts

    The format should be:
    logger.suAlert([tenant_id][version][alertType][subType][complete error/description]);
    """
    _format = "[{tenant_id}][{version}][{alertType}][{subType}][{message}]"
    if self.isEnabledFor(SU_ALERT_LEVEL):
        message = message if isinstance(message, dict) else {"message": message}
        message = _format.format(tenant_id=message.get("tenant_id", "<tenant_id>"),
                                 version=message.get("version", "<version>"),
                                 alertType=message.get("alertType", "<alertType>"),
                                 subType=message.get("subType", "<subType>"),
                                 message=message.get("message", "SUALERT MESSAGE NOT PASSED. Please pass "
                                                                "logger.suAlert({'message': '<Your message here>'})"))
        self._log(SU_ALERT_LEVEL, message, args, **kwargs)


# Add the method to the Logger class
logging.Logger.suAlert = suAlert
