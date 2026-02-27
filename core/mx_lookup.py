import dns.resolver
import dns.exception


def mx_lookup(domain):
    print("\n[+] Fetching MX records...\n")

    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ["8.8.8.8"]
        resolver.timeout = 5
        resolver.lifetime = 5

        answers = resolver.resolve(domain, "MX")

        records = []
        for rdata in answers:
            records.append({
                "priority": rdata.preference,
                "server": str(rdata.exchange).rstrip(".")
            })

        return {
            "MX Records Found": len(records),
            "Records": records
        }

    except dns.resolver.NoAnswer:
        return {"Error": "Domain exists but has no MX records"}

    except dns.resolver.NXDOMAIN:
        return {"Error": "Domain does not exist"}

    except dns.exception.Timeout:
        return {"Error": "DNS query timed out"}

    except Exception as e:
        return {"Error": str(e)}
