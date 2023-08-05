# -*- coding: latin-1 -*-
# -----------------------------------------------------------------------------
# Copyright 2013-2015 Stephen Tiedemann <stephen.tiedemann@gmail.com>
#
# Licensed under the EUPL, Version 1.1 or - as soon they 
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# http://www.osor.eu/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# -----------------------------------------------------------------------------

import logging
log = logging.getLogger(__name__)

class Tag(object):
    """The base class for all NFC Tags/Cards. The methods and attributes
    defined here are commonly available but some may, depending on the
    tag product, also return a :const:`None` value is support is not
    available.

    Direct subclasses are the NFC Forum tag types:
    :class:`~nfc.tag.tt1.Type1Tag`, :class:`~nfc.tag.tt2.Type2Tag`,
    :class:`~nfc.tag.tt3.Type3Tag`, :class:`~nfc.tag.tt4.Type4Tag`.
    Some of them are further specialized in vendor/product specific
    classes.

    """
    class NDEF(object):
        """The NDEF object type that may be read from :attr:`Tag.ndef`.

        This class presents the NDEF management information and the
        actual NDEF message by a couple of attributes. It is normally
        accessed from a :class:`Tag` instance through the
        :attr:`~Tag.ndef` attribute for reading or writing an NDEF
        message. ::

            if tag.ndef is not None:
                print(tag.ndef.message.pretty())
                if tag.ndef.is_writeable:
                    text_record = nfc.ndef.TextRecord("Hello World")
                    tag.ndef.message = nfc.ndef.Message(text_record)

        """
        def __init__(self, tag):
            self._tag = tag
            self._data = None
            self._capacity = 0
            self._readable = False
            self._writeable = False

        def _read_ndef_data(self):
            msg = "_read_ndef_data is not implemented for this tag type"
            raise NotImplementedError(msg)

        def _write_ndef_data(self, data):
            msg = "_write_ndef_data is not implemented for this tag type"
            raise NotImplementedError(msg)

        @property
        def tag(self):
            """A readonly reference to the underlying tag object."""
            return self._tag

        @property
        def length(self):
            """Length of the current NDEF message in bytes."""
            return len(self._data) if self._data else 0
        
        @property
        def capacity(self):
            """Maximum number of bytes for an NDEF message."""
            return self._capacity

        @property
        def is_readable(self):
            """:const:`True` if the NDEF data are is readable."""
            return self._readable

        @property
        def readable(self):
            log.warning("'ndef.readable' is deprecated, use 'is_readable'")
            return self.is_readable

        @property
        def is_writeable(self):
            """:const:`True` if the NDEF data area is writeable."""
            return self._writeable

        @property
        def writeable(self):
            log.warning("'ndef.writeable' is deprecated, use 'is_writeable'")
            return self.is_writeable

        @property
        def has_changed(self):
            """The boolean attribute :attr:`has_changed` allows to determine
            whether the NDEF message on the tag is different from the
            message that was read or written at an earlier time in the
            session. This may for example be the case if the tag is
            build to dynamically present different content depending
            on some state.

            Note that reading this attribute involves a complete
            update of the :class:`~Tag.NDEF` instance accessed through
            :attr:`Tag.ndef`. As a result, it is possible that the
            :attr:`Tag.ndef` attribute may have become :const:`None`
            if there was, for example, now invalid data on the tag. A
            robust implementation should thus verify the value of the
            :attr:`Tag.ndef` attribute. ::

                if tag.ndef.has_changed:
                    if tag.ndef is not None:
                        print(tag.ndef.message.pretty())

            The :attr:`has_changed` attribute can also be used to
            verify that an NDEF message that was written to the tag is
            identical to the NDEF message stored on the tag. ::

                tag.ndef.message = my_new_ndef_message
                if tag.ndef.has_changed:
                    print("the tag data differs from what was written")

            """
            old_data, self._data = self._data, self._read_ndef_data()
            if self._data is None: self._tag._ndef = None
            return self._data != old_data

        @property
        def message(self):
            """Read or write the :class:`nfc.ndef.Message` on the tag.
            
            If valid NDEF data was read from the tag, then
            :attr:`message` holds an :class:`nfc.ndef.Message` object
            representing that data. Otherwise it holds an empty
            message, i.e. an NDEF message that is composed of a single
            NDEF record with type zero, no name (identifier) and no
            data. Note that the :attr:`length` attribute always
            returns the true NDEF data length. ::
            
                empty_message = nfc.ndef.Message(nfc.ndef.Record())
            
                if tag.ndef is not None:
                    print(tag.ndef.message.pretty())
                    if tag.ndef.message == empty_message:
                        if tag.ndef.length == 0:
                            print("there's no data stored on the tag")
                        elif tag.ndef.length == 3:
                            print("looks like an empty message found")
                        else:
                            print("got a message that failed to parse")
            
            """
            import nfc.ndef
            
            if len(self._data) > 3:
                try: return nfc.ndef.Message(str(self._data))
                except nfc.ndef.parser_error as error:
                    log.error(repr(error))

            # return an empty record message
            return nfc.ndef.Message(nfc.ndef.Record())

        @message.setter
        def message(self, msg):
            if not self._writeable:
                raise AttributeError("ndef message is not writeable")
            data = bytearray(str(msg))
            if len(data) > self.capacity:
                raise ValueError("ndef message size exceeds capacity")
            self._write_ndef_data(data)
            self._data = data

    def __init__(self, clf, target):
        self._clf, self._target = (clf, target)
        self._ndef = None
        self._authenticated = False

    def __str__(self):
        """x.__str__() <==> str(x)"""
        try: s = self.type + ' ' + repr(self._product)
        except AttributeError: s = self.type
        return s + ' ID=' + self.identifier.encode("hex").upper()

    @property
    def clf(self):
        return self._clf
        
    @property
    def target(self):
        return self._target
        
    @property
    def type(self):
        return self.TYPE

    @property
    def product(self):
        return self._product if hasattr(self, "_product") else self.type

    @property
    def identifier(self):
        """The unique tag identifier."""
        return str(self._nfcid)

    @property
    def ndef(self):
        """An :class:`NDEF` object if found, otherwise :const:`None`."""
        if self._ndef is None:
            ndef = self.NDEF(self)
            if ndef.has_changed:
                self._ndef = ndef
        return self._ndef

    @property
    def is_present(self):
        """True if the tag is within communication range."""
        return self._is_present()

    @property
    def is_authenticated(self):
        """True if the tag was successfully authenticated."""
        return bool(self._authenticated)
        
    def dump(self):
        """The dump() method returns a list of strings describing the memory
        structure of the tag, suitable for printing with join(). The
        list format makes custom indentation a bit easier. ::

            print("\\n".join(["\\t" + line for line in tag.dump]))
        
        """
        return []

    def format(self, version=None, wipe=None):
        """Format the tag to make it NDEF compatible or erase content.

        The :meth:`format` method is highly dependent on the tag type,
        product and present status, for example a tag that has been
        made read-only with lock bits can no longer be formatted or
        erased.

        :meth:`format` creates the management information defined by
        the NFC Forum to describes the NDEF data area on the tag, this
        is also called NDEF mapping. The mapping may differ between
        versions of the tag specifications, the mapping to apply can
        be specified with the *version* argument as an 8-bit integer
        composed of a major version number in the most significant 4
        bit and the minor version number in the least significant 4
        bit. If *version* is not specified then the highest possible
        mapping version is used.

        If formatting of the tag is possible, the default behavior of
        :meth:`format` is to update only the management information
        required to make the tag appear as NDEF compatible and empty,
        previously existing data could still be read. If existing data
        shall be overwritten, the *wipe* argument can be set to an
        8-bit integer that will be written to all available bytes.

        The :meth:`format` method returns :const:`True` if formatting
        was successful, :const:`False` if it failed for some reason,
        or :const:`None` if the present tag can not be formatted
        either because the tag does not support formatting or it is
        not implemented in nfcpy.

        """
        if hasattr(self, "_format"):
            args = "version={0!r}, wipe={1!r}"
            args = args.format(version, wipe)
            log.debug("format({0})".format(args))
            status = self._format(version, wipe)
            if status is True: self._ndef = None
            return status
        else:
            log.debug("this tag can not be formatted with nfcpy")
            return None

    def protect(self, password=None, read_protect=False, protect_from=0):
        """Protect a tag against future write or read access.

        :meth:`protect` attempts to make a tag readonly for all
        readers if *password* is :const:`None`, writeable only after
        authentication if a *password* is provided, and readable only
        after authentication if a *password* is provided and the
        *read_protect* flag is set. The *password* must be a byte or
        character sequence that provides sufficient key material for
        the tag specific protect function (this is documented
        separately for the individual tag types). As a special case,
        if *password* is set to an empty string the :meth:`protect`
        method uses a default manufacturer value if such is known.

        The *protect_from* argument sets the first memory unit to be
        protected. Memory units are tag type specific, for a Type 1 or
        Type 2 Tag a memory unit is 4 byte, for a Type 3 Tag it is 16
        byte, and for a Type 4 Tag it is the complete NDEF data area.

        Note that the effect of protecting a tag without password can
        normally not be reversed.

        The return value of :meth:`protect` is either :const:`True` or
        :const:`False` depending on whether the operation was
        successful or not, or :const:`None` if the tag does not
        support custom protection (or it is not implemented).
        
        """
        if hasattr(self, "_protect"):
            args = "password={0!r}, read_protect={1!r}, protect_from={2!r}"
            args = args.format(password, read_protect, protect_from)
            log.debug("protect({0})".format(args))
            status = self._protect(password, read_protect, protect_from)
            if status is True: self._ndef = None
            return status
        else:
            log.error("this tag can not be protected with nfcpy")
            return None

    def authenticate(self, password):
        """Authenticate a tag with a *password*.

        A tag that was once protected with a password requires
        authentication before write, potentially also read, operations
        may be performed. The *password* must be the same as the
        password provided to :meth:`protect`. The return value
        indicates authentication success with :const:`True` or
        :const:`False`. For a tag that does not support authentication
        the return value is :const:`None`.

        """
        if hasattr(self, "_authenticate"):
            args = "password={0!r}".format(password)
            log.debug("authenticate({0})".format(args))
            self._authenticated = self._authenticate(password)
            if self._authenticated is True: self._ndef = None
            return self._authenticated
        else:
            log.error("this tag can not be authenticated with nfcpy")
            return None

TIMEOUT_ERROR = 0
RECEIVE_ERROR = -1
PROTOCOL_ERROR = -2

class TagCommandError(Exception):
    """The base class for exceptions that are raised when a tag command
    has not returned the expected result or a a lower stack error was
    raised.

    The :attr:`errno` attribute holds a reason code for why the
    command has failed. Error numbers greater than zero indicate a tag
    type specific error from one of the exception classes derived from
    :exc:`TagCommandError` (per tag type module). Error numbers below
    and including zero indicate general errors::
    
        nfc.tag.TIMEOUT_ERROR  => unrecoverable timeout error
        nfc.tag.RECEIVE_ERROR  => unrecoverable transmission error
        nfc.tag.PROTOCOL_ERROR => unrecoverable protocol error
    
    The :exc:`TagCommandError` exception populates the *message*
    attribute of the general exception class with the appropriate
    error description.

    """
    errno_str = {
        TIMEOUT_ERROR: "unrecoverable timeout error",
        RECEIVE_ERROR: "unrecoverable transmission error",
        PROTOCOL_ERROR: "unrecoverable protocol error",
    }
    
    def __init__(self, errno):
        default = "tag command error {errno} (0x{errno:x})".format(errno=errno)
        if errno > 0: message = self.errno_str.get(errno, default)
        else: message = TagCommandError.errno_str.get(errno, default)
        super(TagCommandError, self).__init__(message)
        self._errno = errno

    @property
    def errno(self):
        """Holds the error reason code."""
        return self._errno

    def __int__(self):
        return self._errno

def activate(clf, target):
    import nfc.clf
    try:
        log.debug("trying to activate {0}".format(target))
        if target.brty.endswith('A'):
            if target.sens_res[1] & 0x0F == 0x0C:
                return activate_tt1(clf, target)
            elif target.sel_res[0] >> 5 & 3 == 0:
                return activate_tt2(clf, target)
            elif target.sel_res[0] >> 5 & 1 == 1:
                return activate_tt4(clf, target)
        elif target.brty.endswith('B'):
            return activate_tt4(clf, target)
        elif target.brty.endswith('F'):
            return activate_tt3(clf, target)
    except nfc.clf.CommunicationError:
        return None

def activate_tt1(clf, target):
    log.debug("trying type 1 tag activation for {0}".format(target.brty))
    import nfc.tag.tt1
    return nfc.tag.tt1.activate(clf, target)
    
def activate_tt2(clf, target):
    log.debug("trying type 2 tag activation for {0}".format(target.brty))
    import nfc.tag.tt2
    return nfc.tag.tt2.activate(clf, target)
    
def activate_tt3(clf, target):
    log.debug("trying type 3 tag activation for {0}".format(target.brty))
    import nfc.tag.tt3
    return nfc.tag.tt3.activate(clf, target)
    
def activate_tt4(clf, target):
    log.debug("trying type 4 tag activation for {0}".format(target.brty))
    import nfc.tag.tt4
    return nfc.tag.tt4.activate(clf, target)

class TagEmulation(object):
    """Base class for tag emulation classes."""
    pass

def emulate(clf, target):
    import nfc.clf
    assert isinstance(target, nfc.clf.LocalTarget)
    if target.tt3_cmd:
        import nfc.tag.tt3
        return nfc.tag.tt3.Type3TagEmulation(clf, target)
    else:
        log.debug("can't emulate with %s", target)

