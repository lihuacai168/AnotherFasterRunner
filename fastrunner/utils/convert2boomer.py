import json
from enum import Enum
from typing import Optional

from pydantic import BaseModel, conint

from fastrunner.utils.convert2hrp import Hrp


class JsonValueType(str, Enum):
    int: str = "int"
    intArray: str = "intArray"
    string: str = "string"
    interface: str = "interface"


class BoomerExtendCmd(BaseModel):
    max_rps: int | None
    master_host: str = "10.129.144.24"
    master_port: int = 5557
    json_value_type: str = JsonValueType.interface.value
    replace_str_index: dict
    disable_keepalive: conint(gt=0, lt=1) = 0
    cpu_profile: str | None
    cpu_profile_duration: int | None
    mem_profile: str | None
    mem_profile_duration: int | None


class BoomerIn(BaseModel):
    faster_request: dict
    extend_cmd: BoomerExtendCmd
    verbose: conint(gt=0, lt=1) = 0


class Boomer:
    def __init__(self, hrp: Hrp, extend_cmd: BoomerExtendCmd):
        self.hrp = hrp
        self.extend_cmd = extend_cmd

    def to_boomer_cmd(self, verbose: bool = True) -> str:
        data_path: str = "/home/toc/SDE/code/locust-boomer/data.csv"
        image = "boomer:latest"
        end = " \\\n"
        base_cmd = f"docker run -v {data_path}:/app/data.csv {image}{end}"
        req_cmd = ""
        for k, v in self.hrp.get_request().dict().items():
            if isinstance(v, (dict, list)):
                v = f"'{json.dumps(v, indent=4)}'"
            if isinstance(v, bool):
                v = 1 if v else 0

            if isinstance(v, (str, int)):
                v = f"{v}{end}"

            if k == "url":
                req_cmd += f"--{k}={v}"
            if k == "method":
                req_cmd += f"--{k}={v}"
            if k == "headers":
                req_cmd += f"--json-headers={v}"
            if k == "req_json":
                req_cmd += f"--raw-data={v}"
        cmd = f"{base_cmd}{req_cmd}"

        for k, v in self.extend_cmd.dict().items():
            if isinstance(v, (str, int)):
                v = f"{v}{end}"
            if k == "master_host":
                cmd += f"--master-host={v}"
            if k == "master_port":
                cmd += f"--master-port={v}"
            if k == "disable-keepalive" and v:
                cmd += "--disable-keepalive 1"
            if k == "max_rps" and v is not None:
                cmd += f"--max-rps={v}"
            if k == "json_value_type":
                cmd += f"--json-value-type={v}"
            if k == "replace_str_index":
                cmd += f"--replace-str-index='{json.dumps(v, indent=4)}'{end}"

        if verbose:
            cmd += "--verbose 1"
        if cmd[-1] == "\\":
            cmd = cmd[:-1]
        return cmd
