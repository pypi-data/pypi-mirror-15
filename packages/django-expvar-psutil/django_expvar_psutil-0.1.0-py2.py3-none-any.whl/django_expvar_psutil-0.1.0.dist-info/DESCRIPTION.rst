psutil plugin for [django-expvar](https://github.com/thraxil/django-expvar/)

* pip install it
* add `expvarpsutil` to `INSTALLED_APPS`

exposes everything that it can glean from
[psutil](https://github.com/giampaolo/psutil).

Sample output:


    {
    "vmem": {
         "available": 21817942016,
         "used": 29588267008,
         "cached": 14833836032,
         "percent": 35.2,
         "free": 4071620608,
         "inactive": 11338760192,
         "active": 16109834240,
         "total": 33659887616,
         "buffers": 2912485376},
	"netio": {
         "dropin": 10,
         "packets_recv": 5051051546,
         "bytes_recv": 16324722441209,
         "dropout": 0,
         "bytes_sent": 14774021978712,
         "errout": 0,
         "packets_sent": 4435177714,
         "errin": 52},
	"swap": {
         "used": 6767640576,
         "percent": 21.0,
         "free": 25397030912,
         "sout": 140025290752,
         "total": 32164671488,
         "sin": 178708295680},
    "cpu": {
         "guest": 0.0,
         "irq": 113.01,
         "system": 907022.44,
         "idle": 42276546.24,
         "user": 5368869.44,
         "iowait": 7038784.66,
         "nice": 1194231.6,
         "steal": 0.0,
         "softirq": 63126.39}
	}


