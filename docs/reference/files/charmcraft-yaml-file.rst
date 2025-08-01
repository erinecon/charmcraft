.. _charmcraft-yaml-file:

``charmcraft.yaml`` file
========================

..
    AUTHOR NOTE:
    The full list of keys is defined in the Charmcraft project (but this implies upstream keys from craft-application):
    https://github.com/canonical/charmcraft/blob/3.2.0/charmcraft/models/project.py#L381-L1070

    The parts key connects to an external library. The plugin properties are defined here: https://canonical-craft-parts.readthedocs-hosted.com/en/latest/reference/part_properties.html

    This test file shows the full spec at once: https://github.com/canonical/charmcraft/blob/main/tests/unit/models/valid_charms_yaml/full.yaml

.. important::

    ``charmcraft.yaml`` is the only ``yaml`` file generated by ``charmcraft init`` and
    the only ``yaml`` file in a charm project that a charm author should edit directly.

    Charmcraft will use the information you provide here to generate
    :ref:`actions-yaml-file`, :ref:`config-yaml-file`, and :ref:`metadata-yaml-file`,
    as well as all the other files it usually does.

``charmcraft.yaml`` is a file in your charm project that contains keys that allow you
to declare information about the project in a form that can be used by Charmcraft.

.. collapse:: Expand to view a full charm with sample content all at once

    .. literalinclude:: charmcraft-sample-charm.yaml
        :language: yaml


.. _charmcraft-yaml-key-actions:

``actions``
-----------

    Definition owned by `Juju`_. Used by `Charmcraft`_, `Charmhub`_, `Juju`_.

**Status:** Optional.

**Purpose:** Defines actions the charm can take.

**Name:** String = user-defined action name.

**Value:** Mapping.

The value of this key is the contents of :ref:`actions-yaml-file`.

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :language: yaml
        :start-at: actions:
        :end-before: analysis:

.. admonition:: Best practice
    :class: hint

    Prefer lowercase alphanumeric names, and use hyphens (-) to separate words. For
    charms that have already standardised on underscores, it is not necessary to
    change them, and it is better to be consistent within a charm then to have
    some action names be dashed and some be underscored.


.. _charmcraft-yaml-key-analysis:

``analysis``
------------

    Definition owned by `Charmcraft`_. Used by `Charmcraft`_.

**Status:** Optional.

**Purpose:** Defines how the analysis done on the package will behave. This analysis
is run implicitly as part of the ``pack`` command but can be called explicitly with
the ``charmcraft analyse`` command.

**Structure:**

.. code-block:: yaml

    analysis:
      ignore:
        attributes: [<check-name>,...]
        linters: [<check-name>,...]

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: analysis:
        :end-before: assumes:


.. _charmcraft-yaml-key-assumes:

``assumes``
-----------

**Status:** Optional. Recommended for Kubernetes charms.

**Purpose:** Allows charm authors to explicitly state in the metadata of a charm
various features that a Juju model must be able to provide to ensure that the charm
can be successfully deployed on it. When a charm comes preloaded with such
requirements, this enables Juju to perform a pre-deployment check and to display
user-friendly error messages if a feature requirement cannot be met by the model
that the user is trying to deploy the charm to. If the assumes section of the charm
metadata is omitted, Juju will make a best-effort attempt to deploy the charm, and
users must rely on the output of ``juju status`` to figure out whether the deployment
was successful.

**Structure:** The key consists of a list of features that can be given either
directly or, depending on the complexity of the condition you want to enforce,
nested under one or both of the boolean expressions ``any-of`` or ``all-of``, as
shown below. In order for a charm to be deployed, all entries in the ``assumes``
block must be satisfied.

.. code-block:: yaml

    assumes:
     - <feature>
     - any-of:
       - <feature>
       - <feature>
     - all-of:
       - <feature>
       - <feature>

.. This should really go into the Juju docs, as they are the ones who parse it.

.. list-table:: Supported features

    * - Structure
      - Description
      - Examples
      - Juju versions
    * - ``juju <comparison predicate> <version number>``
      - The charm deploys `iff`_ the model runs agent binaries with the specified
        Juju version(s).
      - ``juju >= 3.0``
        ``juju < 4.0``
      - Since 2.9.23
    * - ``k8s-api``
      - The charm deploys `iff`_ the :external+juju:ref:`backing cloud <cloud>`
        for the model is Kubernetes.
      - ``k8s-api``
      - Since Juju 2.9.23

.. collapse:: Simple example

    .. code-block:: yaml

        assumes:
         - juju >= 2.9.23
         - k8s-api

.. collapse:: Complex example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: assumes:
        :end-before: base:


.. _charmcraft-yaml-base:
.. _charmcraft-yaml-key-base:

``base``
--------

**Status:** Required in most cases if `type`_ is ``charm``.

**Purpose:** Specifies the operating system on which the charm will build and run.

**Structure:**

.. code-block:: yaml

    base: <distro>@<series>

**Example:**

.. code-block:: yaml

    base: ubuntu@24.04


.. _charmcraft-yaml-key-bases:

``bases``
---------

.. note::

    ``bases`` is deprecated, replaced by `base`_, `build-base`_, and platforms.

    .. collapse:: See more

        The ``bases`` key is only accepted for bases supported before 2024-01-01.

        .. code-block:: yaml

            # The run time base, the base format is <os-name>@<os-release>,
            # accepted bases are:
            # - ubuntu@22.04
            # - ubuntu@24.04
            base: <base>
            # The build time base. Only used if the runtime base is not stable.
            # Accepts all runtime bases and ``ubuntu@devel``
            build-base: <base>

            # The supported platforms
            platforms:
              <platform-name>:
                build-on: <list-of-arch> | <arch>
                build-for: <list-of-arch> | <arch>

**Status:** Deprecated. Conflicts with the `base`_, `build-base`_, and platforms
keys.

**Purpose:** Specifies a list of environments (OS version and architecture)
where the charm must be built on and run on.

**Structure:** This key supports a list of bases where the charm can be built,
and where that build can run. Each item can be expressed using two different
internal structures, a short and a long form. The long one is more explicit:

.. code-block:: yaml

    bases:
      - build-on:
          - name: <name>
            channel: <channel>
            architectures:
              - <arch>
        run-on:
          - name: <name>
            channel: <channel>
            architectures:
              - <arch>

The ``run-on`` part of each entry is optional and defaults to what's specified
in the corresponding ``build-on``. In both structures the list of architecture
strings is also optional, defaulting to the architecture of the current machine.

The short form is more concise and simple (at the cost of being less flexible):

.. code-block:: yaml

    bases:
      - name: <name>
        channel: <channel>
        architectures:
          - <arch>

It implies that the specified base is to be used for both ``build-on`` and
``run-on``. As above, the list of architecture strings is also optional, defaulting
to the machine architecture.

.. collapse:: Example

    .. code-block:: yaml

        bases:
          - build-on:
              - name: ubuntu
                channel: '22.04'
                architectures:
                  - amd64
                  - riscv64
              - name: ubuntu
                channel: '20.04'
                architectures:
                  - amd64
                  - arm64
            run-on:
              - name: ubuntu
                channel: '22.04'
                architectures:
                  - amd64
              - name: ubuntu
                channel: '22.04'
                architectures:
                  - riscv64
              - name: ubuntu
                channel: '22.04'
                architectures:
                  - arm64
          - build-on:
              - name: ubuntu
                channel: '24.04'
            run-on:
              - name: ubuntu
                channel: '24.04'
                architectures:
                  - amd64
                  - arm64
                  - riscv64
                  - s390x
                  - ppc64el
                  - armhf


.. _charmcraft-yaml-key-build-base:

``build-base``
--------------

**Status:** Only valid if `base`_ is a development base.

**Purpose:** Specifies the operating system on which the charm will be built.

**Structure:**

.. code-block:: yaml

    build-base: <distro>@<series>

**Example:**

.. code-block:: yaml

    base: ubuntu@devel


.. _charmcraft-yaml-key-charm-libs:

``charm-libs``
--------------

**Status:** Optional.

**Purpose:** Declares charm libraries for Charmcraft to include in the charm
project. For each lib, include both the lib name (in ``<charm>.<library>`` format)
and the lib version (in ``"<api version>[.<patch version>]"`` string format).

**Structure:**

.. code-block:: yaml

    charm-libs:
      - lib: <charm>.<library>
        version: "<api>[.<patch>]"  # Must be a string, not a number.

**Example:**

.. literalinclude:: charmcraft-sample-charm.yaml
    :start-at: charm-libs:
    :end-before: charm-user:


.. _charmcraft-yaml-key-charm-user:

``charm-user``
--------------

.. important::

    ``charm-user`` was added in Juju 3.6.0. It's currently only supported by
    Kubernetes charms and has no effect on machine charms.

**Status:** Optional. Recommended for Kubernetes charms.

**Purpose:** The ``charm-user`` key  allows charm authors to specify that their charm
hook code does not need to be run as root. This key, in combination with ``uid`` and
``gid`` fields in ``containers``, allows the charm to be run rootless. If set to
``root``, the charm runs as root. If set to ``sudoer`` or ``non-root``, the charm runs
as a user other than root. If the value is ``sudoer``, the charm will be run as a user
with access to sudo to elevate its privileges.

**Structure:** The key consists of a single value. One of ``root``, ``sudoer`` or
``non-root``.

.. code-block:: yaml

    # (Optional) What kind of user is required to run the charm code.
    # It can be one of root, sudoer or non-root.
    # Added in Juju 3.6.0. If not specified, root is assumed.
    charm-user: <one of root, sudoer or non-root>

**Example:**

.. literalinclude:: charmcraft-sample-charm.yaml
    :start-at: charm-user:
    :end-before: config:


.. _charmcraft-yaml-key-charmhub:

``charmhub``
------------

.. caution::

    This key is only meaningful in Charmcraft 2. Use the environment variables
    ``CHARMCRAFT_STORE_API_URL``, ``CHARMCRAFT_UPLOAD_URL`` and
    ``CHARMCRAFT_REGISTRY_URL`` for newer versions of Charmcraft.


**Status:** Deprecated and nonfunctional in Charmcraft 3.

**Purpose:** Configures Charmcraft's interaction with store servers.

**Structure:** This key allows for the configuration of three values---the base
URL for the Charmhub API, the base URL to push binaries to Charmhub and the URL
of the container registry for OCI image uploads. These keys are also optional.

.. code-block:: yaml

    charmhub:
      api-url: <api url>
      storage-url: <storage url>
      registry-url: <registry url>

The key is used mostly in the context of "private" charm stores, defaulting to
the standard Canonical services to operate with charms.

.. collapse:: Example

    .. code-block:: yaml

        charmhub:
          api-url: https://api.staging.charmhub.io
          storage-url: https://storage.staging.snapcraftcontent.com


.. _charmcraft-yaml-key-config:

``config``
----------

    See first: :external+juju:ref:`Juju | Application configuration
    <application-configuration>`

**Status:** Optional.

**Purpose:** Creates user-facing configuration options for the charm.

**Structure:**

.. code-block:: yaml

    config:
      options:
        # Each option name is the name by which the charm will query the option.
        <option name>:
          # (Required) The type of the option
          type: string | int | float | boolean | secret
          # (Optional) The default value of the option
          default: <a reasonable default value of the same type as the option>
          # (Optional): A string describing the option. Also appears on charmhub.io
          description: <description string>

If ``type`` is ``secret``, this is a string that needs to correspond to the
secret URI.

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: config:
        :end-before: containers:

.. admonition:: Best practice
    :class: hint

    Just like Juju, a charm is an opinionated tool. Configure the application
    with the best defaults (ideally the application is deployable without
    providing any configuration at deploy time), and only expose application
    configuration options when necessary.

.. admonition:: Best practice
    :class: hint

    Prefer lowercase alphanumeric names, separated with dashes if required. For
    charms that have already standardised on underscores, it is not necessary to
    change them, and it is better to be consistent within a charm then to have
    some config names be dashed and some be underscored.

.. admonition:: Best practice
    :class: hint

    For very complex applications, consider providing configuration profiles,
    which can group values for large configs together. For example,
    a ``profile: large`` that tweaks multiple options under the hood to optimize for
    larger deployments, or a ``profile: ci`` for limited resource usage during
    testing.


.. _charmcraft-yaml-key-containers:

``containers``
--------------

**Status:** Required for Kubernetes charms (except for proxy charms running on
Kubernetes).

**Purpose:** The ``containers`` key allows you to define a map of containers to be
created adjacent to the charm (as a sidecar, in the same pod).

**Structure:** This key consists of a list of containers along with their
specification. Each container can be specified in terms of ``resource``, ``bases``,
``uid``, ``gid`` and ``mounts``, where one of either the ``resource`` or the
``bases`` subkeys must be defined, and ``mounts`` is optional. ``resource`` stands
for the OCI image resource used to create the container; to use it, specify  an OCI
image resource name (that you will then define further in the `resources`_ block).
``bases`` is a list of bases to be used for resolving a container image, in descending
order of preference; to use it, specify a base name (for example, ``ubuntu``,
``centos``, ``osx``, ``opensuse``), a
`channel <https://snapcraft.io/docs/channels>`_, and an architecture. ``mounts`` is a
list of mounted storages for this container; to use it, specify the name of the
storage to mount from the charm storage and, optionally, the location where to mount
the storage. Starting with Juju 3.5.0, ``uid`` and ``gid`` are the UID and,
respectively, GID to run the Pebble entry process for this container as; they can
be any value from 0-999 or any value from 10,000 (values from 1000-9999 are reserved
for users) and the default is 0 (root).

.. code-block:: yaml

    containers:
      <container name>:
        resource: <resource name>
        bases:
          - name: <base name>
            channel: <track[/risk][/branch]>
            architectures:
              - <architecture>
        mounts:
          - storage: <storage name>
            location: <path>
        uid: <unix UID>
        gid: <unix GID>

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: containers:
        :end-before: description:


.. _charmcraft-yaml-key-description:

``description``
---------------

**Status:** Required if the `type`_ key is set to ``charm``. Recommended otherwise.

**Example:**

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: description: |
        :end-before: devices:


.. _charmcraft-yaml-key-devices:

``devices``
-----------

**Status:** Optional

**Purpose:** Defines the device requests for the charm, for example a GPU.

**Structure:**

.. code-block:: yaml

    devices:
        # Each key represents the name of the device
        <device name>:
            # (Required) The type of device requested
            type: gpu | nvidia.com/gpu | amd.com/gpu
            # (Optional) Description of the requested device
            description: <description>
            # (Optional) Minimum number of devices required
            countmin: <n>
            # (Optional) Maximum number of devices required
            countmax: <n>

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: devices:
        :end-before: extra-bindings:


.. _charmcraft-yaml-key-extra-bindings:

``extra-bindings``
------------------

**Status:** Optional.

**Purpose:** Extra bindings for the charm. For example binding extra network interfaces.

**Structure:**  A key-only map; key represents the name of the binding:

.. code-block:: yaml

    extra-bindings:
      <binding name>:

**Example:**

.. literalinclude:: charmcraft-sample-charm.yaml
    :start-at: extra-bindings:
    :end-before: links:


.. _charmcraft-yaml-key-links:
.. _charmcraft-yaml-key-links-contact:
.. _charmcraft-yaml-key-links-source:
.. _charmcraft-yaml-key-links-issues:
.. _charmcraft-yaml-key-links-website:
.. _charmcraft-yaml-key-contact:
.. _charmcraft-yaml-key-documentation:


``links``
---------

**Status:** Optional. Recommended.

**Purpose:** Links to various additional information, to be displayed on Charmhub.

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: links:
        :end-before: name:

.. admonition:: Best practice
    :class: hint

    Documentation links should apply to the charm, and not to the application that
    is being charmed. Assume that the user already has basic competency in the use
    of the application.

.. _charmcraft-yaml-key-name:

``name``
--------

**Status:** Required if the `type`_ key is set to ``charm``.

**Purpose:** The name of the charm. Determines the ``.charm`` file name and, if the
charm is published on Charmhub, the charm page URL in Charmhub. As a result, it also
determines the name administrators will ultimately use to deploy the charm. E.g.
``juju deploy <name>``.

**Structure:**

.. code-block:: yaml

    name: <name>

**Example:**

.. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: name:
        :end-before: parts:

.. admonition:: Best practice
    :class: hint

    The name should be slug-oriented (ASCII lowercase letters, numbers, and
    hyphens) and follow the pattern ``<workload name in full>[<function>][-k8s]``.
    For example, ``argo-server-k8s``.

    Include the ``-k8s`` suffix on all charms that run on a Kubernetes cloud,
    unless the charm has no workload or you know that there will never be
    a machine version of the charm.

    Don't include an organization or publisher in the name.

    Don't add an ``operator`` or ``charm`` prefix or suffix. For naming a
    repository, see :ref:`initialise-a-charm`.


.. _charmcraft-yaml-key-parts:

``parts``
---------

**Status:** Recommended.

**Purpose:** Configures the various mechanisms to obtain, process and prepare
data from different sources that end up being a part of the final charm.

**Structure:** Mapping. Keys are user-defined part names. The value of each key
is a map where keys are part properties.

..     https://github.com/canonical/charmcraft/issues/2378
..     See more: :ref:`part_properties`

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: parts:
        :end-before: peers:

.. collapse:: Details

    .. TODO: These should be moved to their own plugin pages.

    Charmcraft offers three custom parts plugins specifically for writing charms:

    **The** ``charm`` **plugin**

    Used to pack a Charm that is based on the `Operator framework`_.

    Supports the following configuration:

    .. code-block:: yaml

        parts:
          my-charm:
            plugin: charm
            charm-entrypoint: <path to an entrypoint script>
            charm-requirements: <list of requirements files>
            charm-python-packages: <list of package names>
            charm-binary-python-packages: <list of package names>
            prime: <list of paths to extra files>

    In detail:

    - ``charm-entrypoint``: The charm entry point, relative to the project directory. It is optional if not defined defaults to ``src/charm.py``.
    - ``charm-requirements``: A list of requirements files specifying Python dependencies. It is optional; if not defined, defaults to a list with one ``requirements.txt`` entry if that file is present in the project directory.
    - ``charm-python-packages``: A list of Python packages to install before installing requirements. These packages will be installed from sources and built locally at packing time. It is optional, defaults to empty.
    - ``charm-binary-python-packages``: A list of python packages to install before installing requirements and regular Python packages. Binary packages are allowed, but they may also be installed from sources if a package is only available in source form. It is optional, defaults to empty.

    **The** ``reactive`` **plugin**

    Used to pack charms using the reactive framework.

    ..  important::

        The reactive framework has been superseded by the `Operator framework`_.
        Please use that framework instead of reactive. Support for reactive in
        Charmcraft is only to ease the transition of old charms to the new framework.

    Supports the following configuration:

    .. code-block:: yaml

        parts:
          charm:
            source: .
            plugin: reactive
            build-snaps: [charm]
            reactive-charm-build-arguments: <list of command line options>

    The ``reactive_charm_build_arguments`` allows to include extra command line arguments in the underlying ``charm build`` call.


.. _charmcraft-yaml-key-peers:
.. _charmcraft-yaml-key-provides:
.. _charmcraft-yaml-key-requires:

``peers``, ``provides``, and ``requires``
-----------------------------------------

    See also: :external+juju:ref:`Juju | Relation (integration) <relation>`

.. collapse:: Example featuring all three keys

    .. code-block:: yaml

        peers:
          friend:
            interface: life
            limit: 150
            optional: true
            scope: container
        provides:
          self:
            interface: identity
        requires:
          parent:
            interface: birth
            limit: 2
            optional: false
            scope: global


.. collapse:: The full schema for a chosen endpoint role

    .. code-block:: yaml

        <endpoint role>: # 'peers', 'provides', or 'requires'
          # Each key represents the name of the endpoint as known by this charm
          <endpoint name>:
            # (Required) The interface schema that this relation conforms to
            interface: <endpoint interface name>

            # (Optional) Maximum number of supported connections to this relation
            # endpoint. This field is an integer
            limit: <n>

            # (Optional) Defines if the relation is required. Not enforced by
            # Juju, but used by other tools and should always be included.
            optional: true | false

            # (Optional) The scope of the relation. Defaults to "global"
            scope: global | container


``<endpoint role>``
-------------------

**Status:** If you want to define any kind of integration, required.

**Purpose:** To define an integration endpoint.

**Structure:**

*Name:* Depending on what kind of an integration you are trying to define:
``peers``, ``provides``, or ``requires``.

*Type:* Map.

*Value:* One or more key-value pairs denoting a relation and its associated
properties.


``<endpoint role>.<endpoint name>``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Status:** Required.

**Purpose:** To define the name of the relation as known by this charm.

**Structure:**

*Name: User-defined.*

*Type:* string.


``<endpoint role>.<endpoint name>.interface``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Status:** Required.

**Purpose:** To define the interface schema that this relation conforms to.

**Structure:**

*Type:* String.

*Value:* The name of the interface. Usually defined by the author of the charm
providing the interface.  Cannot be ``juju``. Cannot begin with ``juju-``. Must
only contain characters ``a-z`` and ``-`` and cannot start with ``-``.

.. caution::

    The interface name is the only means of establishing whether two charms are
    compatible for integration; and carries with it nothing more than a mutual
    promise that the provider and requirer know the communication protocol implied
    by the name.


``<endpoint role>.<endpoint name>.limit``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Status:** Optional.

**Purpose:** To define the maximum number of supported connections to this relation
endpoint.

**Structure:**

*Type:* Integer.

``<endpoint role>.<endpoint name>.optional``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Status:** Optional.

**Purpose:** To define if the relation is required. Not enforced by Juju.

**Structure:**

*Type:* Boolean.

*Default value:* ``false``

.. admonition:: Best practice
    :class: hint

    Always include the ``optional`` key, rather than relying on the default
    value to indicate that the relation is required. Although this field is
    not enforced by Juju, including it makes it clear to users (and other tools)
    whether the relation is required.


``<endpoint role>.<endpoint name>.scope``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Status:** Optional.

**Purpose:** To define the scope of the relation, that is, the set of units from
integrated applications that are reported to the unit as members of the integration.

**Structure:**

*Type:* String.

**Possible values:** ``container``, ``global``.

Container-scoped integrations are restricted to reporting details of a single
principal unit to a single subordinate, and vice versa, while global integrations
consider all possible remote units. Subordinate charms are only valid if they have
at least one ``requires`` integration with ``container`` scope.

**Default value:** ``global``.



.. _charmcraft-yaml-key-resources:

``resources``
-------------

    See first: :external+juju:ref:`Juju | Resource (charm) <charm-resource>`

**Status:** Optional.

**Purpose:**  To define a resource for your charm.

.. note::
    Kubernetes charms must declare an ``oci-image`` resource for each container
    they define in the `containers`_  mapping.

**Structure:**

.. code-block:: yaml

    resources:
      <resource-name>:
        type: <file> or <oci-image>
        description: <string description of the resource>
        filename: <path to resource if it is a file>

.. collapse:: File resource example


    .. code-block:: yaml

        resources:
          water:
            type: file
            filename: /dev/h2o

.. collapse:: OCI image example

    .. code-block:: yaml

        resources:
          super-app-image:
            type: oci-image
            description: OCI image for the Super App (hub.docker.com/_/super-app)



.. _charmcraft-yaml-key-storage:

``storage``
-----------

**Status:** Optional.

**Purpose:** Storage requests for the charm.

**Structure:**

.. code-block:: yaml

    storage:
      # Each key represents the name of the storage
      <storage name>:

        # (Required) Type of the requested storage
        # The filesystem type requests a directory in which the charm may store files.
        # If the storage provider only supports provisioning disks, then a disk will be
        # created, attached, partitiioned, and a filesystem created on top, and the
        # filesystem will be presented to the charm as normal.
        # The block type requests a raw block device, typically disks or logical volumes.
        type: filesystem | block

        # (Optional) Description of the storage requested
        description: <description>

        # (Optional) The mount location for filesystem stores. For multi-stores
        # the location acts as the parent directory for each mounted store.
        location: <location>

        # (Optional) Indicates if the storage should be made read-only (where possible)
        read-only: true | false

        # (Optional) The number of storage instances to be requested
        multiple:
            range: <n> | <n>-<m> | <n>- | <n>+

        # (Optional) Minimum size of requested storage in forms G, GiB, GB. Size
        # multipliers are M, G, T, P, E, Z or Y. With no multiplier supplied, M
        # is implied.
        minimum-size: <n>| <n><multiplier>

        # (Optional) List of properties, only supported value is "transient"
        properties:
          - transient


.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: storage:  # Possible storage for the charm
        :end-before: subordinate:


.. _charmcraft-yaml-key-subordinate:

``subordinate``
---------------

**Status:** Optional.

**Purpose:** Configures whether the charm is meant to be deployed as a subordinate
to a principal charm.

**Structure:**

.. code-block:: yaml

    subordinate: true | false

**Example:**

.. code-block:: yaml

    subordinate: false


.. _charmcraft-yaml-key-summary:

``summary``
-----------

**Status:** Required if the :ref:`charmcraft-yaml-key-type` key is set to ``charm``.

**Structure:** A short, one-line description of the charm. No more than 78 characters.

.. collapse:: Example

    .. code-block:: yaml

        summary: A Juju charm to run a Traefik-powered ingress controller on Kubernetes.


.. _charmcraft-yaml-key-terms:

``terms``
---------

**Status:** Optional.

**Purpose:** Lists the terms that any charm user agree to when they're using the charm.

**Structure:** The list of terms:

.. code-block:: yaml

    terms:
      - <term>

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: terms:
        :end-before: title: My awesome charm


.. _charmcraft-yaml-key-title:

``title``
---------

**Status:** Optional, but recommended

**Purpose:** A human-readable name for your charm

.. collapse:: Example

    .. literalinclude:: charmcraft-sample-charm.yaml
        :start-at: title:
        :end-before: type:


.. _charmcraft-yaml-key-type:

``type``
--------

**Status:** Required.

**Purpose:** Indicates the type of package charmcraft will pack.

**Structure:**

**Type:** String.

**Value:** ``charm``.

.. collapse:: Example

    .. code-block:: yaml

        type: charm

.. _iff: https://en.wikipedia.org/wiki/If_and_only_if
