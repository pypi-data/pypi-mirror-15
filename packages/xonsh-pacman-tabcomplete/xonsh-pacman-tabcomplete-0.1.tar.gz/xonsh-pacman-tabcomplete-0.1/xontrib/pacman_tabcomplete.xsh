def search_pacman(query, installed=True, remote=False):
    results = set()
    #splitting leaves every other line with package version info
    if installed:
        package_list = $(pacman -Q).split()[::2]
    elif not remote:
        package_list = full_list(remote=False)
    else:
        package_list = full_list(remote)
    for package_name in package_list:
        if package_name.startswith(query):
            results.add(package_name)

    return results


def full_list(remote=False):
    if remote:
        package_list = [pac.split('/')[-1].split(' ')[0] for a in $(pacman -Ss).split('\n')[::2]]
    else:
        package_list = [pac.split('/')[-1].split(' ')[0] for a in $(pacman -Qs).split('\n')[::2]]

    return package_list


def pacman_completer(prefix, line, begidx, endidx, ctx):
    """
    Completes pacman remove command with installed package names
    """
    if 'pacman' and '-R' in line:
        return search_pacman(prefix)
    elif 'pacman' and '-Ss' in line:
        return search_pacman(prefix, installed=False, remote=True)
    elif 'pacman' and '-Qs' in line:
        return search_pacman(prefix, installed=False, remote=False)

#add to list of completers
__xonsh_completers__['pacman'] = pacman_completer
#bump to top of list (otherwise bash completion interferes)
__xonsh_completers__.move_to_end('pacman', last=False)
