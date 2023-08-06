# Copyright 2016 Osvaldo Santana Neto
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import List, TypeVar, Union

from correios.exceptions import InvalidZipCodeException, InvalidStateException, InvalidTrackingCode


ZIP_CODE_LENGTH = 8
STATE_LENGTH = 2
TRACKING_CODE_SIZE = 13
TRACKING_CODE_NUMBER_SIZE = 8
TRACKING_CODE_PREFIX_SIZE = 2
TRACKING_CODE_SUFFIX_SIZE = 2


class ZipCode(object):
    def __init__(self, code: str):
        self._code = self._validate(code)

    @property
    def code(self) -> str:
        return self._code

    def _validate(self, code) -> str:
        code = "".join(d for d in code if d.isdigit())

        if len(code) != ZIP_CODE_LENGTH:
            raise InvalidZipCodeException("ZipCode code must have 8 digits")

        return code

    def display(self) -> str:
        return "{}-{}".format(self.code[:5], self.code[-3:])

    def __eq__(self, other):
        return self._code == self._validate(other)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<ZipCode code: {}>".format(self.code)


class State(object):
    STATES = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins',
    }
    _name_map = {v.lower(): k for k, v in STATES.items()}

    def __init__(self, code: str):
        self._code = self._validate(code)

    @property
    def code(self) -> str:
        return self._code

    def _validate(self, raw_state) -> str:
        state = self._name_map.get(raw_state.lower(), raw_state)
        state = state.upper()

        if len(state) != STATE_LENGTH or state not in self.STATES:
            raise InvalidStateException("State code {} is invalid".format(state))

        return state

    def display(self):
        return self.STATES[self.code]

    def __eq__(self, other):
        return self.code == self._validate(other)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<State code: {} name: {}>".format(self.code, self.display())


StateType = TypeVar("StateType", State, str)


class ZipAddress(object):
    # noinspection PyShadowingBuiltins
    def __init__(self,
                 id: int,
                 zip_code: Union[ZipCode, str],
                 state: StateType,
                 city: str,
                 district: str,
                 address: str,
                 complements: List[str]):
        self.id = id
        self.zip_code = ZipCode(str(zip_code))
        self.state = State(str(state))
        self.city = city
        self.district = district
        self.address = address
        self.complements = [c for c in complements if c]


class TrackingCode(object):
    def __init__(self, code: str):
        self.prefix = code[:2].upper()
        self.number = "".join(d for d in code[2:10] if d.isdigit())
        self.suffix = code[-2:].upper()
        self._digit = None

        if len(code) == TRACKING_CODE_SIZE and code[10:11] != " ":
            self._digit = int(code[10:11])

        self._validate()

    def _validate(self):
        if len(self.prefix) != TRACKING_CODE_PREFIX_SIZE or not self.prefix.isalpha():
            raise InvalidTrackingCode("Invalid tracking code prefix {}".format(self.prefix))

        if len(self.suffix) != TRACKING_CODE_SUFFIX_SIZE or not self.suffix.isalpha():
            raise InvalidTrackingCode("Invalid tracking code suffix {}".format(self.suffix))

        if len(self.number) != TRACKING_CODE_NUMBER_SIZE or not self.number.isnumeric():
            raise InvalidTrackingCode("Invalid tracking code number {}".format(self.number))

        if self._digit is not None and self._digit != self.calculate_digit(self.number):
            raise InvalidTrackingCode("Invalid tracking code number {} or digit {} (must be {})".format(
                self.number,
                self._digit,
                self.calculate_digit(self.number))
            )

    def calculate_digit(self, number: str) -> int:
        numbers = [int(c) for c in number if c.isdigit()]

        multipliers = [8, 6, 4, 2, 3, 5, 9, 7]
        module = sum(multipliers[i] * digit for i, digit in enumerate(numbers)) % 11

        if not module:
            return 5

        if module == 1:
            return 0

        return 11 - module

    @property
    def digit(self):
        if self._digit is None:
            self._digit = self.calculate_digit(self.number)
        return self._digit

    @property
    def code(self):
        return self.prefix + self.number + str(self.digit) + self.suffix

    @property
    def nodigit(self):
        return "{}{} {}".format(self.prefix, self.number, self.suffix)

    @property
    def short(self):
        return "{}{}{}".format(self.prefix, self.number, self.suffix)

    def __str__(self):
        return self.code
