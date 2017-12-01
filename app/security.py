
def manager_check(user):
    return user.isManager()

def privileged_check(user):
    return user.isManager() or user.isOfficer()

def officer_check(user):
    return user.isOfficer()
