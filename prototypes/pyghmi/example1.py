from pyghmi.ipmi import command
from pyghmi.exceptions import IpmiException

# Usage: boot_res = doIPMICommand(boot, bootDev)

def doIPMICommand(req, func):
    retry = 1
    chk = checkUUID(req, False)
    if not chk.status: return chk
    req.user = _bot_user
    details = getDeviceDetails(req)
    #return details
    if not details.status: return details
    details.data = details.data[req.uuid]
    if not "ipmi_host" in details.data: return fail(msg="No available IPMI Host", error=ErrorCode.NO_IPMI_HOST)

    ipmi_host = details.data.ipmi_host

    try:
        ipmi_user = details.data.ipmi_user
        ipmi_pass = details.data.ipmi_pass
    except:
        return fail(msg="Invalid IPMI Config!", error=ErrorCode.NO_IPMI_HOST)

    cmd = None
    result = fail(msg="Something went terribly wrong")

    def callFunc(req, cmd, retry):
        try:
            retry = retry + 1
            error(req.uuid + ": Retry Attempt - " + str(retry))
            # error(retry)

            cmd = command.Command(bmc=ipmi_host, userid=ipmi_user, password=ipmi_pass)
            result = func(req, cmd)
            error(result)
        except IpmiException, e:
            if retry != 60:
                time.sleep(30)
                result = callFunc(req, cmd, retry)
            else:
                result = fail(msg=str(e))

        return result

    try:
        cmd = command.Command(bmc=ipmi_host, userid=ipmi_user, password=ipmi_pass)
        # try:
        result = func(req, cmd)
        # except Exception, e:
        #     result = fail(msg="Test")
    except IpmiException, e:
        time.sleep(30)
        result = callFunc(req, cmd, retry)
    finally:
        if cmd:
            cmd.ipmi_session.logout()
    error(req.uuid + ": Return result")
    error(result)
