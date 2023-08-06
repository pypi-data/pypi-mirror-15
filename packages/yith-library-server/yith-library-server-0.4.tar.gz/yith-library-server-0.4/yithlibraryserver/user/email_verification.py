# Yith Library Server is a password storage server.
# Copyright (C) 2012-2013 Yaco Sistemas
# Copyright (C) 2012-2013 Alejandro Blanco Escudero <alejandro.b.e@gmail.com>
# Copyright (C) 2012-2015 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of Yith Library Server.
#
# Yith Library Server is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yith Library Server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yith Library Server.  If not, see <http://www.gnu.org/licenses/>.

import uuid

from sqlalchemy.orm.exc import NoResultFound

from pyramid_sqlalchemy import Session

from yithlibraryserver.email import send_email
from yithlibraryserver.user.models import User


class EmailVerificationCode(object):

    def __init__(self, code=None):
        if code is None:
            self.code = self._generate_code()
        else:
            self.code = code

    def _generate_code(self):
        return str(uuid.uuid4())

    def verify(self, email):
        try:
            return Session.query(
                User
            ).filter(
                User.email == email,
                User.email_verification_code == self.code
            ).one()
        except NoResultFound:
            return None

    def send(self, request, user, url):
        context = {
            'link': '%s?code=%s&email=%s' % (url, self.code, user.email),
            'user': user,
        }
        return send_email(
            request,
            'yithlibraryserver.user:templates/email_verification_code',
            context,
            'Please verify your email address',
            [user.email],
        )
