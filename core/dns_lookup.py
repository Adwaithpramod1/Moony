import dns.resolver

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8', '1.1.1.1']

def dns_lookup(domain):
    print("\n[+] DNS Lookup...\n")
    records = {}
    record_types = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "PTR"]

    for rtype in record_types:
        try:
            answer = resolver.resolve(domain, rtype)
            formatted = []
            for r in answer:
                ttl = answer.rrset.ttl
                if rtype == "MX":
                    formatted.append(f"{r.exchange} (Preference: {r.preference}) TTL: {ttl}")
                elif rtype == "SOA":
                    formatted.append(f"MNAME: {r.mname}, RNAME: {r.rname}, Serial: {r.serial} TTL: {ttl}")
                elif rtype == "PTR":
                    formatted.append(f"{r.target} TTL: {ttl}")
                else:
                    formatted.append(f"{r} TTL: {ttl}")
            records[rtype] = formatted
            if formatted:
                print(f"{rtype} Records:")
                for rec in formatted:
                    print(f"  - {rec}")
            else:
                print(f"{rtype} Records: None")
        except Exception as e:
            records[rtype] = []
            print(f"{rtype} Records: Error ({e})")
    return records
