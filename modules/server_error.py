#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_server_error(url, base_header, full, authent, url_file):
    """
        Check diff btw server error and basic response
    """
    print("\n\033[36m ├ Server error analyse\033[0m")
    error_header = []
    valid_error = False
    error_length = 0

    payloads_error = ["%2a","%EXT%", "%ff", "%0A", "..%3B/", "..%3B", "%2e"]
    for p in payloads_error:
        url_error = "{}{}".format(url,p) if url[-1] else "{}/{}".format(url,p)
        try:
            req_error = requests.get(url_error, verify=False, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko'}, timeout=10, auth=authent)

            if req_error.status_code in [400, 500] and not valid_error:
                print(" i - 400 error code with {} payload [{} bytes]".format(p, len(req_error.content)))
                
                if error_length != len(req_error.content):
                    error_length = len(req_error.content)
                    valid_error = True

                for re in req_error.headers:
                    error_header.append("{}: {}".format(re, req_error.headers[re]))
                for eh in error_header:
                    if eh not in base_header:
                        # IDK why but the map or lambda fctn seem bad with threading...
                        if not url_file:
                            error_header = list(map(lambda x: x.replace(eh, "\033[33m{}\033[0m".format(eh)), error_header))
                        else:
                            pass

                if len(error_header) < len(base_header):
                    while len(error_header) != len(base_header):
                        error_header.append("")
                print("")
                print(f" \033[36m200 response header\033[0m {' ':<25} \033[36m400 response header\033[0m")
                for pbh, peh in zip(base_header, error_header):
                    if not full:
                        pbh = pbh.replace(pbh[40:], "...") if len(pbh) > 40 else pbh
                        peh = peh.replace(peh[60:], "...\033[0m") if len(peh) > 60 else peh
                    print(' {pbh:<45} → {peh:<15}'.format(pbh=pbh, peh=peh))
                print("")
            else:
                pass
        except:
            print(" ! Error with {} payload".format(p))
    header_cache_error(url, authent)


def header_cache_error(url, authent):
        headers = {"\\":"1"}
        try:
            hce_req = requests.get(url, headers=headers, verify=False, timeout=10, auth=authent)
            if hce_req.status_code == 400:
                print(" i - 400 error code with {} payload header [{} bytes]".format(headers, len(hce_req.content)))
                #print(hce_req.headers)
        except:
            print(" i - Error code with {} payload header ".format(headers))
