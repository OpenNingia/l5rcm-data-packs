# -*- coding: iso-8859-1 -*-
# Copyright (C) 2014 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# check if the dal has corrected data

import dal
import sys
import os
import re

def printe(*args):
    sys.stderr.write(*args)
    sys.stderr.write('\n')

class DataCheck(object):

    def __init__(self, path=None, includes=None):

        if not includes:
            includes = []

        if not path:
            path = './data_packs'

        self.path = path
        self.includes = includes

    def check(self):

        try:
            self.ref = dal.Data([self.path] + self.includes, log=False)
            self.d = dal.Data([self.path], log=False)
        except dal.DataPackLoadingError as e:
            printe("E] XML data is malformed")
            printe( str(e) )
            return False
        except Exception as e:
            printe("E] Generic error")
            printe( str(e) )
            return False

        if not self.check_manifest(self.path):
            return False

        self.tags =  [ x.id for x in self.ref.clans    ]
        self.tags += [ x.id for x in self.ref.families ]
        for s in self.ref.schools:
            self.tags += s.tags

        self.check_many(self.d.skills, self.check_skill, 'skill'    )
        self.check_many(self.d.merits, self.check_perk , 'merit'    )
        self.check_many(self.d.flaws , self.check_perk , 'flaw'     )
        self.check_many(self.d.families, self.check_family, 'family')
        self.check_many(self.d.schools,  self.check_school, 'school')

    def check_many(self, items, func, name):
        for i in items:
            if not func(i):
                print("ERR> <{0}> {1}\n".format(name, i.id))

    def check_manifest(self, root_path):
        manifest_file = os.path.join(root_path, 'manifest')
        if not os.path.exists(manifest_file):
            printe("E] Manifest not found")
            return False

        if len(self.d.packs) != 1:
            printe("E] Manifest not valid")
            return False

        dm = self.d.packs[0]

        if not dm.display_name:
            print("W] Missing 'display_name' in manifest")

        if not dm.version:
            print("W] Missing 'version' in manifest")

        if not len(dm.authors):
            print("W] Missing 'authors' in manifest")

        if not dm.min_cm_ver:
            print("W] Missing 'min_cm_ver' in manifest")

        rx_version = re.compile(r'\d{1,2}\.\d{1,2}(\.\d{1,2})?')

        if dm.version:
            if not rx_version.match(dm.version):
                printe("E] Manifest 'version' format error")
                return False

        if dm.min_cm_ver:
            if not rx_version.match(dm.min_cm_ver):
                printe("E] Manifest 'min_cm_ver' format error")
                return False

        return True

    def check_skill(self, i):
        ret = True
        # check skill category
        if len( [x for x in self.ref.skcategs if x.id == i.type]) == 0:
            printe("E] skill category {0} not found".format(i.type))
            ret = False
        # check skill trait
        if len( [x for x in self.ref.traits if x.id == i.trait] + [x for x in self.ref.rings if x.id == i.trait]) == 0:
            printe("E] skill trait {0} not found".format(i.trait))
            ret = False
        return ret

    def check_perk(self, i):
        ret = True
        # check perk category
        if len( [x for x in self.ref.perktypes if x.id == i.type]) == 0:
            printe("E] perk category {0} not found".format(i.type))
            ret = False

        # check exception tags
        for r in i.ranks:
            for e in r.exceptions:
                if e.tag not in self.tags:
                    printe("E] perk exception tag {0} not found".format(e.tag))
                    ret = False
        return ret

    def check_family(self, i):
        ret = True
        #check clanid
        if len( [x for x in self.d.clans if x.id == i.clanid]) == 0:
            printe("E] clan {0} not found".format(i.clanid))
            ret = False
        return ret

    def check_school(self, i):
        ret = True
        #check clanid
        if len( [x for x in self.ref.clans if x.id == i.clanid]) == 0:
            printe("E] clan {0} not found".format(i.clanid))
            ret = False
        # check  trait
        if len( [x for x in self.ref.traits if x.id == i.trait] + ['void']) == 0:
            printe("E] school trait {0} not found".format(i.trait))
            ret = False

        # check affinity and deficiency
        if len( [x for x in self.ref.rings if x.id == i.affinity] + ['void']) == 0:
            printe("E] element {0} not found (affinity)".format(i.trait))
            ret = False
        if len( [x for x in self.ref.rings if x.id == i.deficiency] + ['void']) == 0:
            printe("E] element {0} not found (deficiency)".format(i.trait))
            ret = False

        is_path_or_advanced = 'advanced' in i.tags or 'alternate' in i.tags

        # check honor value
        #if i.honor == 0.0 and not is_path_or_advanced:
        #    print("W] warning. honor 0.0 can be a parsing error. school {0}".format(i.id))

        # check skills
        for s in i.skills:
            if len( [x for x in self.ref.skills if x.id == s.id]) == 0:
                printe("E] skill {0} not found".format(s.id))
                ret = False

        # check outfit
        if len(i.outfit) == 0 and not is_path_or_advanced:
            print("W] Missing outfit, school: {0}".format(i.id))

        # check tech description
        for t in i.techs:
            if len(t.desc.strip()) == 0:
                print("W] Missing technique description: {0}".format(t.id))

        return ret


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Check data package content.')
    parser.add_argument('-I', type=str, nargs='+',
                        dest="includes",
                        metavar="INCLUDE",
                        help='include packages with referenced content')
    parser.add_argument('-P', type=str,
                        dest="package",
                        metavar="PACKAGE",
                        help='path to the package to check')

    return parser.parse_args()


def main(args):
    dc = DataCheck(args.package, args.includes)
    print("*** START")
    dc.check()
    print("      END ***")


if __name__ == "__main__":
    main(parse_args())