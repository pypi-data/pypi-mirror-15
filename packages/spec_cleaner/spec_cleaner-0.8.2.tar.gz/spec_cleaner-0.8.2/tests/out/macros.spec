#
# spec file for package macros
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%build
# FIXME: you should use %%cmake macros
cmake . \
	-DIHATECMAKE=OFF
# FIXME: you should use the %%configure macro
./configure --with-bells-and-whistles
# this is not autotools
./configure --aughr

%changelog
