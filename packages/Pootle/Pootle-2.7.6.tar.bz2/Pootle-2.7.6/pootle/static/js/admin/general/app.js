/*
 * Copyright (C) Pootle contributors.
 *
 * This file is a part of the Pootle project. It is distributed under the GPL3
 * or later license. See the LICENSE file for a copy of the license and the
 * AUTHORS file for copyright and authorship information.
 */

import dashboard from './dashboard';
import permissions from './permissions';
import staticpages from './staticpages';

window.PTL = window.PTL || {};


PTL.commonAdmin = {

  init(opts) {
    switch (opts.page) {
      case 'dashboard':
        dashboard.init();
        break;
      case 'permissions':
        permissions.init();
        break;
      case 'staticpages':
        staticpages.init(opts.opts);
        break;
    }
  },

};
