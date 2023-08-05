#!/usr/bin/env python
#
# Copyright (c) 2012 Eran Sandler (eran@sandler.co.il),  http://eran.sandler.co.il,  http://forecastcloudy.net
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import urllib2
import argparse
import datetime
import re
import demjson

EC2_REGIONS = [
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "eu-west-1",
    "eu-central-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "sa-east-1"
]

EC2_INSTANCE_TYPES = [
    "t1.micro",
    "m1.small",
    "m1.medium",
    "m1.large",
    "m1.xlarge",
    "m2.xlarge",
    "m2.2xlarge",
    "m2.4xlarge",

    "t2.micro",
    "t2.small",
    "t2.medium",

    "m3.medium",
    "m3.large",
    "m3.xlarge",
    "m3.2xlarge",

    "c1.medium",
    "c1.xlarge",

    "c3.large",
    "c3.xlarge",
    "c3.2xlarge",
    "c3.4xlarge",
    "c3.8xlarge",

    "cc2.8xlarge",
    "cg1.4xlarge",
    "cr1.8xlarge",
    "hi1.4xlarge",
    "hs1.8xlarge",

    "g2.2xlarge",

    "r3.large",
    "r3.xlarge",
    "r3.2xlarge",
    "r3.4xlarge",
    "r3.8xlarge",

    "i2.xlarge",
    "i2.2xlarge",
    "i2.4xlarge",
    "i2.8xlarge",

    "d2.xlarge",
    "d2.2xlarge",
    "d2.4xlarge",
    "d2.8xlarge",

    "c4.large",
    "c4.xlarge",
    "c4.2xlarge",
    "c4.4xlarge",
    "c4.8xlarge"
]

EC2_OS_TYPES = [
    "linux",       # api platform name = "linux"
    "mswin",       # api platform name = "windows"
    "rhel",        # api platform name = ""
    "sles",        # api platform name = ""
    "mswinSQL",    # api platform name = "windows"
    "mswinSQLWeb", # api platform name = "windows"
]

JSON_NAME_TO_EC2_REGIONS_API = {
    "us-east" : "us-east-1",
    "us-east-1" : "us-east-1",
    "us-west" : "us-west-1",
    "us-west-1" : "us-west-1",
    "us-west-2" : "us-west-2",
    "eu-ireland" : "eu-west-1",
    "eu-west-1" : "eu-west-1",
    "eu-central-1" : "eu-central-1",
    "apac-sin" : "ap-southeast-1",
    "ap-southeast-1" : "ap-southeast-1",
    "ap-southeast-2" : "ap-southeast-2",
    "apac-syd" : "ap-southeast-2",
    "apac-tokyo" : "ap-northeast-1",
    "ap-northeast-1" : "ap-northeast-1",
    "sa-east-1" : "sa-east-1",
    "us-gov-west-1" : "us-gov-west-1"
}

EC2_REGIONS_API_TO_JSON_NAME = {
    "us-east-1" : "us-east",
    "us-west-1" : "us-west",
    "us-west-2" : "us-west-2",
    "eu-west-1" : "eu-ireland",
    "eu-central-1" : "eu-central-1",
    "ap-southeast-1" : "apac-sin",
    "ap-southeast-2" : "apac-syd",
    "ap-northeast-1" : "apac-tokyo",
    "sa-east-1" : "sa-east-1",
    "us-gov-west-1" : "us-gov-west-1"
}

INSTANCES_ON_DEMAND_LINUX_URL = "http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js"
INSTANCES_ON_DEMAND_RHEL_URL = "http://a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js"
INSTANCES_ON_DEMAND_SLES_URL = "http://a0.awsstatic.com/pricing/1/ec2/sles-od.min.js"
INSTANCES_ON_DEMAND_WINDOWS_URL = "http://a0.awsstatic.com/pricing/1/ec2/mswin-od.min.js"
INSTANCES_ON_DEMAND_WINSQL_URL = "http://a0.awsstatic.com/pricing/1/ec2/mswinSQL-od.min.js"
INSTANCES_ON_DEMAND_WINSQLWEB_URL = "http://a0.awsstatic.com/pricing/1/ec2/mswinSQLWeb-od.min.js"
INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/linux-ri-light.js"
INSTANCES_RESERVED_LIGHT_UTILIZATION_RHEL_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/rhel-ri-light.js"
INSTANCES_RESERVED_LIGHT_UTILIZATION_SLES_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/sles-ri-light.js"
INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswin-ri-light.js"
INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQL_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswinSQL-ri-light.js"
INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQLWEB_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswinSQLWeb-ri-light.js"
INSTANCES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/linux-ri-medium.js"
INSTANCES_RESERVED_MEDIUM_UTILIZATION_RHEL_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/rhel-ri-medium.js"
INSTANCES_RESERVED_MEDIUM_UTILIZATION_SLES_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/sles-ri-medium.js"
INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswin-ri-medium.js"
INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQL_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswinSQL-ri-medium.js"
INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQLWEB_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswinSQLWeb-ri-medium.js"
INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/linux-ri-heavy.js"
INSTANCES_RESERVED_HEAVY_UTILIZATION_RHEL_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/rhel-ri-heavy.js"
INSTANCES_RESERVED_HEAVY_UTILIZATION_SLES_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/sles-ri-heavy.js"
INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswin-ri-heavy.js"
INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQL_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswinSQL-ri-heavy.js"
INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQLWEB_URL = "http://aws-assets-pricing-prod.s3.amazonaws.com/pricing/ec2/mswinSQLWeb-ri-heavy.js"

INSTANCES_ONDEMAND_OS_TYPE_BY_URL = {
    INSTANCES_ON_DEMAND_LINUX_URL : "linux",
    INSTANCES_ON_DEMAND_RHEL_URL : "rhel",
    INSTANCES_ON_DEMAND_SLES_URL : "sles",
    INSTANCES_ON_DEMAND_WINDOWS_URL : "mswin",
    INSTANCES_ON_DEMAND_WINSQL_URL : "mswinSQL",
    INSTANCES_ON_DEMAND_WINSQLWEB_URL : "mswinSQLWeb",
    }

INSTANCES_RESERVED_OS_TYPE_BY_URL = {
    INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL : "linux",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_RHEL_URL : "rhel",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_SLES_URL : "sles",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL :  "mswin",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQL_URL : "mswinSQL",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQLWEB_URL : "mswinSQLWeb",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL : "linux",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_RHEL_URL : "rhel",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_SLES_URL : "sles",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL :  "mswin",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQL_URL : "mswinSQL",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQLWEB_URL : "mswinSQLWeb",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL : "linux",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_RHEL_URL : "rhel",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_SLES_URL : "sles",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL :  "mswin",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQL_URL : "mswinSQL",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQLWEB_URL : "mswinSQLWeb",
    }

INSTANCES_RESERVED_UTILIZATION_TYPE_BY_URL = {
    INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL : "light",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_RHEL_URL : "light",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_SLES_URL : "light",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL : "light",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQL_URL : "light",
    INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQLWEB_URL : "light",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL : "medium",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_RHEL_URL : "medium",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_SLES_URL : "medium",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL : "medium",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQL_URL : "medium",
    INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQLWEB_URL : "medium",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL : "heavy",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_RHEL_URL : "heavy",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_SLES_URL : "heavy",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL : "heavy",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQL_URL : "heavy",
    INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQLWEB_URL : "heavy",
    }

DEFAULT_CURRENCY = "USD"


class ResultsCacheBase(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ResultsCacheBase, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def get(self, key):
        pass

    def set(self, key, value):
        pass


class SimpleResultsCache(ResultsCacheBase):
    _cache = {}

    def get(self, key):
        if key in self._cache:
            return self._cache[key]

        return None

    def set(self, key, value):
        self._cache[key] = value


class TimeBasedResultsCache(ResultsCacheBase):
    _cache = {}
    _cache_expiration = {}

    # If you wish to chance this expiration use the following (a bit ugly) code:
    #
    # TimeBasedResultsCache()._default_expiration_in_seconds = 86400 # 1 day
    #
    # Since all cache classes inherit from ResultsCacheBase and are singletons that should set it correctly.
    #
    _default_expiration_in_seconds = 3600 # 1 hour

    def get(self, key):
        if key not in self._cache or key not in self._cache_expiration:
            return None

        # If key has expired return None
        if self._cache_expiration[key] < datetime.datetime.utcnow():
            if key in self._cache: del self._cache[key]
            if key in self._cache_expiration: del self._cache_expiration[key]

            return None

        return self._cache[key]

    def set(self, key, value):
        self._cache[key] = value
        self._cache_expiration[key] = datetime.datetime.utcnow() + datetime.timedelta(seconds=self._default_expiration_in_seconds)


def _load_data(url, use_cache=False, cache_class=SimpleResultsCache):
    cache_object = None
    if use_cache:
        cache_object = cache_class()
        result = cache_object.get(url)
        if result is not None:
            return result

    f = urllib2.urlopen(url)
    request = f.read()

    # strip initial comment (with newline)
    modified_request = re.sub(re.compile(r'/\*.*\*/\n', re.DOTALL), '', request)
    # strip from front of request
    modified_request = re.sub(r'^callback\(', '', modified_request)
    # strip from end of request
    modified_request = re.sub(r'\);*$', '', modified_request)

    json = demjson.decode(modified_request)

    if use_cache:
        cache_object.set(url, json)

    return json

def get_ec2_reserved_instances_prices(filter_region=None, filter_instance_type=None, filter_os_type=None, use_cache=False, cache_class=SimpleResultsCache):
    """ Get EC2 reserved instances prices. Results can be filtered by region """

    get_specific_region = (filter_region is not None)
    # except for us-east-1, reserved instance JSON uses the real region names
    if get_specific_region and filter_region == 'us-east-1':
        filter_region = EC2_REGIONS_API_TO_JSON_NAME[filter_region]
    get_specific_instance_type = (filter_instance_type is not None)
    get_specific_os_type = (filter_os_type is not None)

    currency = DEFAULT_CURRENCY

    urls = [
        INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL,
        INSTANCES_RESERVED_LIGHT_UTILIZATION_RHEL_URL,
        INSTANCES_RESERVED_LIGHT_UTILIZATION_SLES_URL,
        INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL,
        INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQL_URL,
        INSTANCES_RESERVED_LIGHT_UTILIZATION_WINSQLWEB_URL,
        INSTANCES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL,
        INSTANCES_RESERVED_MEDIUM_UTILIZATION_RHEL_URL,
        INSTANCES_RESERVED_MEDIUM_UTILIZATION_SLES_URL,
        INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL,
        INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQL_URL,
        INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINSQLWEB_URL,
        INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL,
        INSTANCES_RESERVED_HEAVY_UTILIZATION_RHEL_URL,
        INSTANCES_RESERVED_HEAVY_UTILIZATION_SLES_URL,
        INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL,
        INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQL_URL,
        INSTANCES_RESERVED_HEAVY_UTILIZATION_WINSQLWEB_URL,
        ]

    result_regions = []
    result_regions_index = {}
    result = {
        "config" : {
            "currency" : currency,
            },
        "regions" : result_regions
    }

    for u in urls:
        os_type = INSTANCES_RESERVED_OS_TYPE_BY_URL[u]
        if get_specific_os_type and os_type != filter_os_type:
            continue
        utilization_type = INSTANCES_RESERVED_UTILIZATION_TYPE_BY_URL[u]
        data = _load_data(u, use_cache=use_cache, cache_class=cache_class)
        if "config" in data and data["config"] and "regions" in data["config"] and data["config"]["regions"]:
            for r in data["config"]["regions"]:
                if "region" in r and r["region"]:
                    if get_specific_region and filter_region != r["region"]:
                        continue

                    region_name = JSON_NAME_TO_EC2_REGIONS_API[r["region"]]
                    if region_name in result_regions_index:
                        instance_types = result_regions_index[region_name]["instanceTypes"]
                    else:
                        instance_types = []
                        result_regions.append({
                            "region" : region_name,
                            "instanceTypes" : instance_types
                        })
                        result_regions_index[region_name] = result_regions[-1]

                    if "instanceTypes" in r:
                        for it in r["instanceTypes"]:
                            instance_type = it["type"]
                            if "sizes" in it:
                                for s in it["sizes"]:
                                    instance_size = s["size"]

                                    prices = {
                                        "1year" : {
                                            "hourly" : None,
                                            "upfront" : None
                                        },
                                        "3year" : {
                                            "hourly" : None,
                                            "upfront" : None
                                        }
                                    }

                                    _type = instance_size
                                    if _type == "cc1.8xlarge":
                                        # Fix conflict where cc1 and cc2 share the same type
                                        _type = "cc2.8xlarge"

                                    # Clean the "*" the appears in the r3 instance
                                    if _type.find("*") > -1:
                                        _type = _type.replace("*", "").strip()

                                    if get_specific_instance_type and _type != filter_instance_type:
                                        continue

                                    if get_specific_os_type and os_type != filter_os_type:
                                        continue

                                    instance_types.append({
                                        "type" : _type,
                                        "os" : os_type,
                                        "utilization" : utilization_type,
                                        "prices" : prices
                                    })

                                    for price_data in s["valueColumns"]:
                                        price = None
                                        try:
                                            price = float(price_data["prices"][currency])
                                        except ValueError:
                                            price = None

                                        if price_data["name"] == "yrTerm1":
                                            prices["1year"]["upfront"] = price
                                        elif price_data["name"] == "yrTerm1Hourly":
                                            prices["1year"]["hourly"] = price
                                        elif price_data["name"] == "yrTerm3":
                                            prices["3year"]["upfront"] = price
                                        elif price_data["name"] == "yrTerm3Hourly":
                                            prices["3year"]["hourly"] = price

    return result

def get_ec2_ondemand_instances_prices(filter_region=None, filter_instance_type=None, filter_os_type=None, use_cache=False, cache_class=SimpleResultsCache):
    """ Get EC2 on-demand instances prices. Results can be filtered by region """

    get_specific_region = (filter_region is not None)
    get_specific_instance_type = (filter_instance_type is not None)
    get_specific_os_type = (filter_os_type is not None)

    currency = DEFAULT_CURRENCY

    urls = [
        INSTANCES_ON_DEMAND_LINUX_URL,
        INSTANCES_ON_DEMAND_RHEL_URL,
        INSTANCES_ON_DEMAND_SLES_URL,
        INSTANCES_ON_DEMAND_WINDOWS_URL,
        INSTANCES_ON_DEMAND_WINSQL_URL,
        INSTANCES_ON_DEMAND_WINSQLWEB_URL
    ]

    result_regions = []
    result = {
        "config" : {
            "currency" : currency,
            "unit" : "perhr"
        },
        "regions" : result_regions
    }

    for u in urls:
        if get_specific_os_type and INSTANCES_ONDEMAND_OS_TYPE_BY_URL[u] != filter_os_type:
            continue

        data = _load_data(u, use_cache=use_cache, cache_class=cache_class)
        if "config" in data and data["config"] and "regions" in data["config"] and data["config"]["regions"]:
            for r in data["config"]["regions"]:
                if "region" in r and r["region"]:
                    if get_specific_region and filter_region != r["region"]:
                        continue

                    region_name = r["region"]
                    instance_types = []
                    if "instanceTypes" in r:
                        for it in r["instanceTypes"]:
                            instance_type = it["type"]
                            if "sizes" in it:
                                for s in it["sizes"]:
                                    instance_size = s["size"]

                                    for price_data in s["valueColumns"]:
                                        price = None
                                        try:
                                            if price_data["prices"][currency]:
                                                price = float(price_data["prices"][currency])
                                        except ValueError:
                                            price = None

                                        _type = instance_size
                                        if _type == "cc1.8xlarge":
                                            # Fix conflict where cc1 and cc2 share the same type
                                            _type = "cc2.8xlarge"

                                        # Clean the "*" the appears in the r3 instance
                                        if _type.find("*") > -1:
                                            _type = _type.replace("*", "").strip()

                                        if get_specific_instance_type and _type != filter_instance_type:
                                            continue

                                        if price_data["name"] == "os":
                                            price_data["name"] = "linux"

                                        if get_specific_os_type and price_data["name"] != filter_os_type:
                                            continue

                                        instance_types.append({
                                            "type" : _type,
                                            "os" : price_data["name"],
                                            "price" : price
                                        })

                        result_regions.append({
                            "region" : region_name,
                            "instanceTypes" : instance_types
                        })

    return result


if __name__ == "__main__":
    def none_as_string(v):
        if not v:
            return ""
        else:
            return v

    try:
        import argparse
    except ImportError:
        print "ERROR: You are running Python < 2.7. Please use pip to install argparse:   pip install argparse"


    parser = argparse.ArgumentParser(add_help=True, description="Print out the current prices of EC2 instances")
    parser.add_argument("--type", "-t", help="Show ondemand or reserved instances", choices=["ondemand", "reserved"], required=True)
    parser.add_argument("--filter-region", "-fr", help="Filter results to a specific region", choices=EC2_REGIONS, default=None)
    parser.add_argument("--filter-type", "-ft", help="Filter results to a specific instance type", choices=EC2_INSTANCE_TYPES, default=None)
    parser.add_argument("--filter-os-type", "-fo", help="Filter results to a specific os type", choices=EC2_OS_TYPES, default=None)
    parser.add_argument("--format", "-f", choices=["json", "table", "csv"], help="Output format", default="table")

    args = parser.parse_args()

    if args.format == "table":
        try:
            from prettytable import PrettyTable
        except ImportError:
            print "ERROR: Please install 'prettytable' using pip:    pip install prettytable"

    data = None
    if args.type == "ondemand":
        data = get_ec2_ondemand_instances_prices(args.filter_region, args.filter_type, args.filter_os_type)
    elif args.type == "reserved":
        data = get_ec2_reserved_instances_prices(args.filter_region, args.filter_type, args.filter_os_type)

    if args.format == "json":
        print demjson.encode(data)
    elif args.format == "table":
        x = PrettyTable()

        if args.type == "ondemand":
            try:
                x.set_field_names(["region", "type", "os", "price"])
            except AttributeError:
                x.field_names = ["region", "type", "os", "price"]

            try:
                x.aligns[-1] = "l"
            except AttributeError:
                x.align["price"] = "l"

            for r in data["regions"]:
                region_name = r["region"]
                for it in r["instanceTypes"]:
                    x.add_row([region_name, it["type"], it["os"], none_as_string(it["price"])])
        elif args.type == "reserved":
            try:
                x.set_field_names(["region", "type", "os", "utilization", "term", "price", "upfront"])
            except AttributeError:
                x.field_names = ["region", "type", "os", "utilization", "term", "price", "upfront"]

            try:
                x.aligns[-1] = "l"
                x.aligns[-2] = "l"
            except AttributeError:
                x.align["price"] = "l"
                x.align["upfront"] = "l"

            for r in data["regions"]:
                region_name = r["region"]
                for it in r["instanceTypes"]:
                    for term in it["prices"]:
                        x.add_row([region_name, it["type"], it["os"], it["utilization"], term, none_as_string(it["prices"][term]["hourly"]), none_as_string(it["prices"][term]["upfront"])])

        print x
    elif args.format == "csv":
        if args.type == "ondemand":
            print "region,type,os,price"
            for r in data["regions"]:
                region_name = r["region"]
                for it in r["instanceTypes"]:
                    print "%s,%s,%s,%s" % (region_name, it["type"], it["os"], none_as_string(it["price"]))
        elif args.type == "reserved":
            print "region,type,os,utilization,term,price,upfront"
            for r in data["regions"]:
                region_name = r["region"]
                for it in r["instanceTypes"]:
                    for term in it["prices"]:
                        print "%s,%s,%s,%s,%s,%s,%s" % (region_name, it["type"], it["os"], it["utilization"], term, none_as_string(it["prices"][term]["hourly"]), none_as_string(it["prices"][term]["upfront"]))