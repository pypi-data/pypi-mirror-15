# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""This module corresponds to the sdss directory in idlutils.
"""
import os
import numpy as np
from astropy.extern.six import string_types
from astropy.io import fits
from . import PydlutilsException
#
# Cache for the maskbits file.
#
maskbits = None
#
# Cache the sweep index
#
sweep_cache = {'star': None, 'gal': None, 'sky': None}
#
# Cache sdss_astrombad data
#
opbadfields = None


def default_skyversion():
    """Returns skyversion number to use for photoop imaging.

    Returns
    -------
    :class:`int`
        The default skyversion number.

    Notes
    -----
    The skyversion number is hard-coded to 2.

    Examples
    --------
    >>> from pydl.pydlutils.sdss import default_skyversion
    >>> default_skyversion()
    2
    """
    return 2


def sdss_astrombad(run, camcol, field, photolog_version='dr10'):
    """For a list of RUN, CAMCOL, FIELD, return whether each field has bad
    astrometry.

    Parameters
    ----------
    run, camcol, field : :class:`int` or array of :class:`int`
        Run, camcol and field.  If arrays are passed,
        all must have the same length.
    photolog_version : :class:`str`, optional
        Use this version of photolog to obtain the obBadfields.par file,
        if $PHOTOLOG_DIR is not set.

    Returns
    -------
    :class:`numpy.ndarray` of :class:`bool`
        Array of bool.  ``True`` indicates the field is bad.

    Raises
    ------
    ValueError
        If the sizes of the arrays don't match or if the array values are out
        of bounds.

    Notes
    -----
    Reads data from ``$PHOTOLOG_DIR/opfiles/opBadFields.par``.

    If there is a problem with one camcol, we assume a
    problem with all camcols.

    """
    from astropy.utils.data import download_file
    from .yanny import yanny
    global opbadfields
    #
    # Check inputs
    #
    if isinstance(run, int):
        #
        # Assume all inputs are integers & promote to arrays.
        #
        run = np.array([run], dtype=np.int64)
        camcol = np.array([camcol], dtype=np.int64)
        field = np.array([field], dtype=np.int64)
    else:
        #
        # Check that all inputs have the same shape.
        #
        if run.shape != camcol.shape:
            raise ValueError("camcol.shape does not match run.shape!")
        if run.shape != field.shape:
            raise ValueError("field.shape does not match run.shape!")
    #
    # Check ranges of parameters
    #
    if ((run < 0) | (run >= 2**16)).any():
        raise ValueError("run values are out-of-bounds!")
    if ((camcol < 1) | (camcol > 6)).any():
        raise ValueError("camcol values are out-of-bounds!")
    if ((field < 0) | (field >= 2**12)).any():
        raise ValueError("camcol values are out-of-bounds!")
    #
    # Read the file
    #
    if opbadfields is None:  # pragma: no cover
        if os.getenv('PHOTOLOG_DIR') is None:
            if (photolog_version == 'trunk' or
                    photolog_version.startswith('branches/')):
                iversion = photolog_version
            else:
                iversion = 'tags/'+photolog_version
            baseurl = ('http://www.sdss3.org/svn/repo/photolog/' +
                        '{0}/opfiles/opBadfields.par').format(iversion)
            filename = download_file(baseurl, cache=True)
        else:
            filename = os.path.join(os.getenv('PHOTOLOG_DIR'), 'opfiles',
                            'opBadfields.par')
        astrombadfile = yanny(filename)
        w = ((astrombadfile['BADFIELDS']['problem'] == 'astrom'.encode()) |
            (astrombadfile['BADFIELDS']['problem'] == 'rotator'.encode()))
        opbadfields = astrombadfile['BADFIELDS'][w]
    #
    # opbadfields already has astrom problems selected at this point
    #
    bad = np.zeros(run.shape, dtype=bool)
    for row in opbadfields:
        w = ((run == row['run']) &
        (field >= row['firstfield']) & (field < row['lastfield']))
        if w.any():
            bad[w] = True
    return bad


def sdss_flagexist(flagname, bitname, flagexist=False, whichexist=False):
    """Check for the existence of flags.

    Parameters
    ----------
    flagname : :class:`str`
        The name of a bitmask group. Not case-sensitive.
    bitname : :class:`str` or :class:`list`
        The name(s) of the specific bitmask(s) within the `flagname` group.
    flagexist : :class:`bool`, optional
        If flagexist is True, return a tuple with the second component
        indicating whether the binary flag named `flagname` exists, even
        if `bitname` is wrong.
    whichexist : :class:`bool`, optional
        If whichexist is True, return a list containing existence test results
        for each individual flag.

    Returns
    -------
    :class:`bool` or :func:`tuple`
        A boolean value or a tuple of bool.
    """
    global maskbits
    if maskbits is None:  # pragma: no cover
        maskbits = set_maskbits()
    #
    # Make sure label is a list
    #
    if isinstance(bitname, string_types):
        bitnames = [bitname.upper()]
    else:
        bitnames = [b.upper() for b in bitname]
    f = False
    l = False
    which = [False] * len(bitnames)
    if flagname.upper() in maskbits:
        f = True
        which = [n in maskbits[flagname.upper()] for n in bitnames]
        l = sum(which) == len(which)
    if flagexist and whichexist:
        return (l, f, which)
    elif flagexist:
        return (l, f)
    elif whichexist:
        return (l, which)
    else:
        return l


def sdss_flagname(flagname, flagvalue, concat=False):
    """Return a list of flag names corresponding to the values.

    Parameters
    ----------
    flagname : :class:`str`
        The name of a bitmask group. Not case-sensitive.
    flagvalue : :class:`long`
        The value to be converted into bitmask names.
    concat : :class:`bool`, optional
        If set to ``True``, the list of names is converted to a
        space-separated string.

    Returns
    -------
    :class:`str` or :class:`list`
        The names of the bitmasks encoded in `flagvalue`.

    Raises
    ------
    KeyError
        If `flagname` is invalid

    Examples
    --------
    >>> from pydl.pydlutils.sdss import sdss_flagname
    >>> sdss_flagname('ANCILLARY_TARGET1',2310346608843161600) # doctest: +REMOTE_DATA
    ['BRIGHTGAL', 'BLAZGX', 'ELG']
    """
    global maskbits
    if maskbits is None:  # pragma: no cover
        maskbits = set_maskbits()
    flagu = flagname.upper()
    flagvaluint = np.uint64(flagvalue)
    one = np.uint64(1)
    bits = [bit for bit in range(64)
            if (flagvaluint & (one << np.uint64(bit))) != 0]
    retval = list()
    for bit in bits:
        try:
            f = [x for x in maskbits[flagu].items() if x[1] == bit]
        except KeyError:
            raise KeyError("Unknown flag group {0}!".format(flagu))
        if f:
            retval.append(f[0][0])
    if concat:
        retval = ' '.join(retval)
    return retval


def sdss_flagval(flagname, bitname):
    """Convert bitmask names into values.

    Converts human-readable bitmask names into numerical values.  The inputs
    are not case-sensitive; all inputs are converted to upper case internally.

    Parameters
    ----------
    flagname : :class:`str`
        The name of a bitmask group.
    bitname : :class:`str` or :class:`list`
        The name(s) of the specific bitmask(s) within the `flagname` group.

    Returns
    -------
    :class:`numpy.uint64`
        The value of the bitmask name(s).

    Raises
    ------
    KeyError
        If `flagname` or `bitname` are invalid names.

    Examples
    --------
    >>> from pydl.pydlutils.sdss import sdss_flagval
    >>> sdss_flagval('ANCILLARY_TARGET1',['BLAZGX','ELG','BRIGHTGAL']) # doctest: +REMOTE_DATA
    2310346608843161600
    """
    global maskbits
    if maskbits is None:  # pragma: no cover
        maskbits = set_maskbits()
    #
    # Make sure inlabel is a list
    #
    if isinstance(bitname, string_types):
        bitnames = [bitname.upper()]
    else:
        bitnames = [b.upper() for b in bitname]
    flagu = flagname.upper()
    flagvalue = np.uint64(0)
    for bit in bitnames:
        if flagu in maskbits:
            if bit in maskbits[flagu]:
                flagvalue += np.uint64(2)**np.uint64(maskbits[flagu][bit])
            else:
                raise KeyError("Unknown bit label {0} for flag group {1}!".format(bit, flagu))
        else:
            raise KeyError("Unknown flag group {0}!".format(flagu))
    return flagvalue


def sdss_objid(run, camcol, field, objnum, rerun=301, skyversion=None):
    """Convert SDSS photometric identifiers into CAS-style ObjID.

    Bits are assigned in objid thus:

    ===== ========== ===============================================
    Bits  Name       Comment
    ===== ========== ===============================================
    63    empty      unassigned
    59-62 skyVersion resolved sky version (0-15)
    48-58 rerun      number of pipeline rerun
    32-47 run        run number
    29-31 camcol     camera column (1-6)
    28    firstField [is this the first field in segment?] 0 for now
    16-27 field      field number within run
    0-15  object     object number within field
    ===== ========== ===============================================

    Parameters
    ----------
    run, camcol, field, objnum : :class:`int` or array of int
        Run, camcol, field and object number within field.  If arrays are
        passed, all must have the same length.
    rerun, skyversion : :class:`int` or array of int, optional
        Rerun and skyversion usually don't change very much.  If supplied,
        make sure the size matches all the other values.

    Returns
    -------
    :class:`numpy.ndarray` of :class:`numpy.int64`
        The ObjIDs of the objects.

    Raises
    ------
    ValueError
        If the sizes of the arrays don't match or if the array values are
        out of bounds.

    Notes
    -----
    firstField flag never set.

    Examples
    --------
    >>> from pydl.pydlutils.sdss import sdss_objid
    >>> sdss_objid(3704,3,91,146)
    array([1237661382772195474])
    """
    if skyversion is None:
        skyversion = default_skyversion()
    if isinstance(run, int):
        run = np.array([run], dtype=np.int64)
    if isinstance(camcol, int):
        camcol = np.array([camcol], dtype=np.int64)
    if isinstance(field, int):
        field = np.array([field], dtype=np.int64)
    if isinstance(objnum, int):
        objnum = np.array([objnum], dtype=np.int64)
    if isinstance(rerun, int):
        if rerun == 301:
            rerun = np.zeros(run.shape, dtype=np.int64) + 301
        else:
            rerun = np.array([rerun], dtype=np.int64)
    if isinstance(skyversion, int):
        if skyversion == default_skyversion():
            skyversion = np.zeros(run.shape, dtype=np.int64) + default_skyversion()
        else:
            skyversion = np.array([skyversion], dtype=np.int64)

    #
    # Check that all inputs have the same shape.
    #
    firstfield = np.zeros(run.shape, dtype=np.int64)
    if run.shape != camcol.shape:
        raise ValueError("camcol.shape does not match run.shape!")
    if run.shape != field.shape:
        raise ValueError("field.shape does not match run.shape!")
    if run.shape != objnum.shape:
        raise ValueError("objnum.shape does not match run.shape!")
    if run.shape != rerun.shape:
        raise ValueError("rerun.shape does not match run.shape!")
    if run.shape != skyversion.shape:
        raise ValueError("skyversion.shape does not match run.shape!")
    #
    # Check ranges of parameters
    #
    if ((skyversion < 0) | (skyversion >= 16)).any():
        raise ValueError("skyversion values are out-of-bounds!")
    if ((rerun < 0) | (rerun >= 2**11)).any():
        raise ValueError("rerun values are out-of-bounds!")
    if ((run < 0) | (run >= 2**16)).any():
        raise ValueError("run values are out-of-bounds!")
    if ((camcol < 1) | (camcol > 6)).any():
        raise ValueError("camcol values are out-of-bounds!")
    if ((field < 0) | (field >= 2**12)).any():
        raise ValueError("camcol values are out-of-bounds!")
    if ((objnum < 0) | (objnum >= 2**16)).any():
        raise ValueError("id values are out-of-bounds!")
    #
    # Compute the objid
    #
    objid = ((skyversion << 59) |
        (rerun << 48) |
        (run << 32) |
        (camcol << 29) |
        (firstfield << 28) |
        (field << 16) |
        (objnum))
    return objid


def sdss_sweep_circle(ra, dec, radius, stype='star', allobj=False):
    """Read the SDSS datasweep files and return objects around a location.

    Parameters
    ----------
    ra, dec : :class:`float`
        The sky location to search, J2000 degrees.
    radius : :class:`float`
        The radius around `ra`, `dec` to search.
    stype : :class:`str`, optional
        The type of object to search, 'star', 'gal' or 'sky'.
        The default is 'star'.
    allobj : :class:`bool`, optional
        If set to ``True``, return all objects found, not just SURVEY_PRIMARY.

    Returns
    -------
    :class:`numpy.ndarray`
        The data extracted from the sweep files.

    Raises
    ------
    PydlutilsException
        If :envvar:`PHOTO_SWEEP` is not set.

    Notes
    -----
    Assumes that the sweep files exist in :envvar:`PHOTO_SWEEP` and
    that index files have been created.
    """
    from .. import uniq
    from .spheregroup import spherematch
    global sweep_cache
    #
    # Check values
    #
    if stype not in ('star', 'gal', 'sky'):
        raise ValueError('Invalid type {0}!'.format(stype))
    sweepdir = os.getenv('PHOTO_SWEEP')
    if sweepdir is None:
        raise PydlutilsException('PHOTO_SWEEP is not set!')
    #
    # Read the index
    #
    if sweep_cache[stype] is None:
        indexfile = os.path.join(sweepdir, 'datasweep-index-{0}.fits'.format(stype))
        with fits.open(indexfile) as f:
            sweep_cache[stype] = f[1].data
    index = sweep_cache[stype]
    #
    # Match
    #
    ira = np.array([ra])
    idec = np.array([dec])
    m1, m2, d12 = spherematch(index['RA'], index['DEC'], ira, idec,
                                radius+0.36, maxmatch=0)
    if len(m1) == 0:
        return None
    if not allobj:
        w = index['NPRIMARY'][m1] > 0
        if w.any():
            m1 = m1[w]
        else:
            return None
    #
    # Maximum number of objects
    #
    if allobj:
        n = index['IEND'][m1] - index['ISTART'][m1] + 1
        ntot = (where(n > 0, n, np.zeros(n.shape, dtype=n.dtype))).sum()
    else:
        ntot = index['NPRIMARY'][m1].sum()
    #
    # Find unique run + camcol
    #
    rc = index['RUN'][m1]*6 + index['CAMCOL'][m1] - 1
    isort = rc.argsort()
    iuniq = uniq(rc[isort])
    istart = 0
    objs = None
    nobjs = 0
    for i in range(len(iuniq)):
        iend = iuniq[i]
        icurr = isort[istart:iend]
        #
        # Determine which file and range of rows
        #
        run = index['RUN'][m1[icurr[0]]]
        camcol = index['CAMCOL'][m1[icurr[0]]]
        rerun = index['RERUN'][m1[icurr[0]]]
        fields = index[m1[icurr]]
        ist = fields['ISTART'].min()
        ind = fields['IEND'].max()
        if ind >= ist:
            #
            # Read in the rows of that file
            #
            swfile = os.path.join(os.getenv('PHOTO_SWEEP'), rerun,
                            'calibObj-{0:06d}-{1:1d}-{2}.fits.gz'.format(
                            int(run), int(camcol), stype))
            with fits.open(swfile) as f:
                tmp_objs = f[1].data[ist:ind]
            if tmp_objs.size > 0:
                #
                # Keep only objects within the desired radius
                #
                tm1, tm2, d12 = spherematch(tmp_objs['RA'], tmp_objs['DEC'],
                                            ira, idec, radius, maxmatch=0)
                if len(tm1) > 0:
                    tmp_objs = tmp_objs[tm1]
                    #
                    # Keep only SURVEY_PRIMARY objects by default
                    #
                    if not allobj:
                        w = ((tmp_objs['RESOLVE_STATUS'] &
                            sdss_flagval('RESOLVE_STATUS',
                                        'SURVEY_PRIMARY')) > 0)
                        if w.any():
                            tmp_objs = tmp_objs[w]
                        else:
                            tmp_objs = None
                    if tmp_objs is not None:
                        if objs is None:
                            objs = np.zeros(ntot, dtype=tmp_objs.dtype)
                        objs[nobjs:nobjs+tmp_objs.size] = tmp_objs
                        nobjs += tmp_objs.size
        istart = iend+1
    if nobjs > 0:
        return objs[0:nobjs]
    else:
        return None


def set_maskbits(idlutils_version='v5_5_8', maskbits_file=None):
    """Populate the maskbits cache.

    Parameters
    ----------
    idlutils_version : :class:`str`, optional
        Fetch the sdssMaskbits.par file corresponding to this idlutils version.
    maskbits_file : :class:`str`, optional
        Use an explicit file instead of downloading the official version.
        This should only be used for tests.

    Returns
    -------
    :class:`dict`
        A dictionary of bitmasks suitable for caching.

    Raises
    ------
    URLError
        If the data file could not be retrieved.
    """
    from astropy.utils.data import download_file
    from .yanny import yanny
    if maskbits_file is None:  # pragma: no cover
        if (idlutils_version == 'trunk' or
                idlutils_version.startswith('branches/')):
            iversion = idlutils_version
        else:
            iversion = 'tags/'+idlutils_version
        baseurl = ('http://www.sdss3.org/svn/repo/idlutils/' +
                    '{0}/data/sdss/sdssMaskbits.par').format(iversion)
        filename = download_file(baseurl, cache=True, show_progress=False)
    else:
        filename = maskbits_file
    maskfile = yanny(filename, raw=True)
    #
    # Parse the file & cache the results in maskbits
    #
    maskbits = dict()
    for k in range(maskfile.size('MASKBITS')):
        if maskfile['MASKBITS']['flag'][k] in maskbits:
            maskbits[maskfile['MASKBITS']['flag'][k]][maskfile['MASKBITS']['label'][k]] = maskfile['MASKBITS']['bit'][k]
        else:
            maskbits[maskfile['MASKBITS']['flag'][k]] = {maskfile['MASKBITS']['label'][k]: maskfile['MASKBITS']['bit'][k]}
    if 'MASKALIAS' in maskfile:
        for k in range(maskfile.size('MASKALIAS')):
            maskbits[maskfile['MASKALIAS']['alias'][k]] = maskbits[maskfile['MASKALIAS']['flag'][k]].copy()
    return maskbits
