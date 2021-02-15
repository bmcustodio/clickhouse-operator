import kubectl
import settings


def query(
        chi_name,
        sql,
        with_error=False,
        host="127.0.0.1",
        port="9000",
        user="",
        pwd="",
        ns=settings.test_namespace,
        timeout=60,
        advanced_params="",
        pod="",
        container="clickhouse-pod"
):
    pod_names = kubectl.get_pod_names(chi_name, ns)
    pod_name = pod_names[0]
    for p in pod_names:
        if host in p or p == pod:
            pod_name = p
            break

    pwd_str = "" if pwd == "" else f"--password={pwd}"
    user_str = "" if user == "" else f"--user={user}"

    if with_error:
        return kubectl.launch(
            f"exec {pod_name} -n {ns} -c {container}"
            f" --"
            f" clickhouse-client -mn -h {host} --port={port} {user_str} {pwd_str} {advanced_params}"
            f" --query=\"{sql}\""
            f" 2>&1",
            timeout=timeout,
            ns=ns,
            ok_to_fail=True,
        )
    else:
        return kubectl.launch(
            f"exec {pod_name} -n {ns} -c {container}"
            f" -- "
            f"clickhouse-client -mn -h {host} --port={port} {user_str} {pwd_str} {advanced_params}"
            f"--query=\"{sql}\"",
            timeout=timeout,
            ns=ns,
        )


def query_with_error(
        chi_name,
        sql,
        host="127.0.0.1",
        port="9000",
        user="",
        pwd="",
        ns=settings.test_namespace,
        timeout=60,
        advanced_params="",
        pod="",
        container="clickhouse-pod",
):
    return query(
        chi_name=chi_name,
        sql=sql,
        with_error=True,
        host=host,
        port=port,
        user=user,
        pwd=pwd,
        ns=ns,
        timeout=timeout,
        advanced_params=advanced_params,
        pod=pod,
        container=container
    )
