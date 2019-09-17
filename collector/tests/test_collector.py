import unittest
from unittest.mock import patch, mock_open
import collector

json_response = {
  "drives": [
    {
      "offline": True,
      "hotSpare": True,
      "invalidDriveData": True,
      "available": True,
      "pfa": True,
      "driveRef": "string",
      "status": "optimal",
      "cause": "none",
      "interfaceType": {
        "driveType": "scsi",
        "fibre": [
          {
            "channel": 0,
            "loopID": 0
          }
        ],
        "sas": {
          "deviceName": "string",
          "drivePortAddresses": [
            {
              "channel": 0,
              "portIdentifier": "string"
            }
          ]
        },
        "scsi": {
          "channel": 0,
          "id": 0
        }
      },
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "manufacturer": "string",
      "manufacturerDate": "string",
      "productID": "string",
      "serialNumber": "string",
      "softwareVersion": "string",
      "blkSize": 0,
      "usableCapacity": "string",
      "rawCapacity": "string",
      "worldWideName": "string",
      "currentVolumeGroupRef": "string",
      "sparedForDriveRef": "string",
      "mirrorDrive": "string",
      "nonRedundantAccess": True,
      "workingChannel": 0,
      "volumeGroupIndex": 0,
      "currentSpeed": "speedUnknown",
      "maxSpeed": "speedUnknown",
      "uncertified": True,
      "hasDegradedChannel": True,
      "degradedChannels": [
        0
      ],
      "phyDriveType": "all",
      "spindleSpeed": 0,
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "reserved": "string",
      "phyDriveTypeData": {
        "phyDriveType": "all",
        "sataDriveAttributes": {
          "translatorData": {
            "vendorId": "string",
            "productId": "string",
            "productRevLevel": "string",
            "satType": "unknown"
          },
          "ataDiskModelNumber": "string",
          "ataDiskFwRevision": "string"
        }
      },
      "pfaReason": "unknown",
      "bypassSource": [
        {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        }
      ],
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "fdeCapable": True,
      "fdeEnabled": True,
      "fdeLocked": True,
      "lockKeyID": "string",
      "ssdWearLife": {
        "averageEraseCountPercent": 0,
        "spareBlocksRemainingPercent": 0,
        "isWearLifeMonitoringSupported": True,
        "percentEnduranceUsed": 0
      },
      "driveMediaType": "all",
      "fpgaVersion": "string",
      "protectionInformationCapabilities": {
        "protectionInformationCapable": True,
        "protectionType": "type0Protection"
      },
      "protectionInformationCapable": True,
      "protectionType": "type0Protection",
      "interposerPresent": True,
      "interposerRef": "string",
      "currentCommandAgingTimeout": 0,
      "defaultCommandAgingTimeout": 0,
      "driveTemperature": {
        "currentTemp": 0,
        "refTemp": 0
      },
      "blkSizePhysical": 0,
      "lowestAlignedLBA": "string",
      "removed": True,
      "locateInProgress": True,
      "fipsCapable": True,
      "firmwareVersion": "string",
      "lockKeyIDValue": "string",
      "id": "string"
    }
  ],
  "ibPorts": [
    {
      "interfaceRef": "string",
      "channel": 0,
      "channelPortRef": "string",
      "localIdentifier": 0,
      "globalIdentifier": "string",
      "linkState": "initialize",
      "portState": "unknown",
      "maximumTransmissionUnit": 0,
      "currentSpeed": "speedUnknown",
      "supportedSpeed": [
        "speedUnknown"
      ],
      "currentLinkWidth": "width1x",
      "supportedLinkWidth": [
        "width1x"
      ],
      "currentDataVirtualLanes": 0,
      "maximumDataVirtualLanes": 0,
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "protectionInformationCapable": True,
      "isSRPSupported": True,
      "isISERSupported": True,
      "physPortState": "unknown",
      "oneWayMaxRate": "string",
      "bidirectionalMaxRate": "string",
      "isNVMeSupported": True,
      "controllerId": "string",
      "commandProtocolProperties": [
        {
          "commandProtocol": "unknown",
          "nvmeProperties": {
            "commandSet": "unknown",
            "nvmeofProperties": {
              "provider": "providerUnknown",
              "ibProperties": {
                "ipAddressData": {
                  "addressType": "ipv4",
                  "ipv4Data": {
                    "configState": "unconfigured",
                    "ipv4Address": "string",
                    "ipv4SubnetMask": "string",
                    "ipv4GatewayAddress": "string"
                  },
                  "ipv6Data": {
                    "address": "string",
                    "addressState": {
                      "addressType": "typeInterface",
                      "interfaceAddressState": "unconfigured",
                      "routerAddressState": "unknown"
                    }
                  }
                },
                "listeningPort": 0
              },
              "roceV2Properties": {
                "ipv4Enabled": True,
                "ipv6Enabled": True,
                "ipv4Data": {
                  "ipv4Address": "string",
                  "ipv4AddressConfigMethod": "configDhcp",
                  "ipv4OutboundPacketPriority": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv4VlanId": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv4AddressData": {
                    "configState": "unconfigured",
                    "ipv4Address": "string",
                    "ipv4SubnetMask": "string",
                    "ipv4GatewayAddress": "string"
                  }
                },
                "ipv6Data": {
                  "ipv6LocalAddresses": [
                    {
                      "address": "string",
                      "addressState": {
                        "addressType": "typeInterface",
                        "interfaceAddressState": "unconfigured",
                        "routerAddressState": "unknown"
                      }
                    }
                  ],
                  "ipv6RoutableAddresses": [
                    {
                      "address": "string",
                      "addressState": {
                        "addressType": "typeInterface",
                        "interfaceAddressState": "unconfigured",
                        "routerAddressState": "unknown"
                      }
                    }
                  ],
                  "ipv6PortRouterAddress": {
                    "address": "string",
                    "addressState": {
                      "addressType": "typeInterface",
                      "interfaceAddressState": "unconfigured",
                      "routerAddressState": "unknown"
                    }
                  },
                  "ipv6AddressConfigMethod": "configStatic",
                  "ipv6OutboundPacketPriority": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv6VlanId": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv6HopLimit": 0,
                  "ipv6NdReachableTime": 0,
                  "ipv6NdRetransmitTime": 0,
                  "ipv6NdStaleTimeout": 0,
                  "ipv6DuplicateAddressDetectionAttempts": 0
                },
                "listeningPort": 0
              },
              "fcProperties": {
                "firstBurstDataSupported": True,
                "firstBurstDataLength": 0
              }
            }
          }
        }
      ],
      "niceAddressId": "string",
      "interfaceId": "string",
      "addressId": "string",
      "id": "string"
    }
  ],
  "iscsiPorts": [
    {
      "channel": 0,
      "channelPortRef": "string",
      "tcpListenPort": 0,
      "ipv4Enabled": True,
      "ipv4Data": {
        "ipv4Address": "string",
        "ipv4AddressConfigMethod": "configDhcp",
        "ipv4OutboundPacketPriority": {
          "isEnabled": True,
          "value": 0
        },
        "ipv4VlanId": {
          "isEnabled": True,
          "value": 0
        },
        "ipv4AddressData": {
          "configState": "unconfigured",
          "ipv4Address": "string",
          "ipv4SubnetMask": "string",
          "ipv4GatewayAddress": "string"
        }
      },
      "interfaceData": {
        "type": "unknown",
        "ethernetData": {
          "partData": {
            "vendorName": "string",
            "partNumber": "string",
            "revisionNumber": "string",
            "serialNumber": "string"
          },
          "macAddress": "string",
          "fullDuplex": True,
          "maximumFramePayloadSize": 0,
          "currentInterfaceSpeed": "speedUnknown",
          "maximumInterfaceSpeed": "speedUnknown",
          "linkStatus": "none",
          "supportedInterfaceSpeeds": [
            "speedUnknown"
          ],
          "autoconfigSupport": True,
          "copperCableDiagnosticsSupport": True,
          "operationalInterfaceSpeed": "speedUnknown"
        },
        "infinibandData": {
          "isIser": True
        }
      },
      "interfaceRef": "string",
      "ipv6Enabled": True,
      "ipv6Data": {
        "ipv6LocalAddresses": [
          {
            "address": "string",
            "addressState": {
              "addressType": "typeInterface",
              "interfaceAddressState": "unconfigured",
              "routerAddressState": "unknown"
            }
          }
        ],
        "ipv6RoutableAddresses": [
          {
            "address": "string",
            "addressState": {
              "addressType": "typeInterface",
              "interfaceAddressState": "unconfigured",
              "routerAddressState": "unknown"
            }
          }
        ],
        "ipv6PortRouterAddress": {
          "address": "string",
          "addressState": {
            "addressType": "typeInterface",
            "interfaceAddressState": "unconfigured",
            "routerAddressState": "unknown"
          }
        },
        "ipv6AddressConfigMethod": "configStatic",
        "ipv6OutboundPacketPriority": {
          "isEnabled": True,
          "value": 0
        },
        "ipv6VlanId": {
          "isEnabled": True,
          "value": 0
        },
        "ipv6HopLimit": 0,
        "ipv6NdReachableTime": 0,
        "ipv6NdRetransmitTime": 0,
        "ipv6NdStaleTimeout": 0,
        "ipv6DuplicateAddressDetectionAttempts": 0
      },
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "protectionInformationCapable": True,
      "isIPv6Capable": True,
      "oneWayMaxRate": "string",
      "bidirectionalMaxRate": "string",
      "iqn": "string",
      "controllerId": "string",
      "niceAddressId": "string",
      "interfaceId": "string",
      "addressId": "string",
      "id": "string"
    }
  ],
  "fibrePorts": [
    {
      "channel": 0,
      "loopID": 0,
      "speed": 0,
      "hardAddress": 0,
      "nodeName": "string",
      "portName": "string",
      "portId": "string",
      "topology": "unknown",
      "part": "string",
      "revision": 0,
      "chanMiswire": True,
      "esmMiswire": True,
      "linkStatus": "none",
      "isDegraded": True,
      "speedControl": "unknown",
      "maxSpeed": 0,
      "speedNegError": True,
      "reserved1": "string",
      "reserved2": "string",
      "ddsChannelState": 0,
      "ddsStateReason": 0,
      "ddsStateWho": 0,
      "isLocal": True,
      "channelPorts": [
        {
          "speedDetError": True,
          "manuallyBypassed": True,
          "portNumber": "portUnknown"
        }
      ],
      "currentInterfaceSpeed": "speedUnknown",
      "maximumInterfaceSpeed": "speedUnknown",
      "interfaceRef": "string",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "isTrunkCapable": True,
      "trunkMiswire": True,
      "protectionInformationCapable": True,
      "oneWayMaxRate": "string",
      "bidirectionalMaxRate": "string",
      "fc4Types": [
        "common"
      ],
      "controllerId": "string",
      "niceAddressId": "string",
      "interfaceId": "string",
      "addressId": "string",
      "id": "string"
    }
  ],
  "sasPorts": [
    {
      "channel": 0,
      "currentInterfaceSpeed": "speedUnknown",
      "maximumInterfaceSpeed": "speedUnknown",
      "part": "string",
      "revision": 0,
      "isDegraded": True,
      "iocPort": {
        "parent": {
          "type": "controller",
          "controller": "string",
          "drive": "string",
          "expander": "string",
          "hostBoardRef": "string"
        },
        "attachedDevice": {
          "channel": 0,
          "channelType": "hostside",
          "sasAttachedDeviceData": {
            "type": "unknown",
            "alternateController": "string",
            "drive": "string",
            "expander": "string",
            "remoteHostPortAddress": "string",
            "localController": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            }
          }
        },
        "state": "unknown",
        "miswireType": "none",
        "channelPortRef": "string",
        "sasPhys": [
          {
            "phyIdentifier": 0,
            "isOperational": True
          }
        ],
        "portTypeData": {
          "portType": "endDevice",
          "portIdentifier": "string",
          "routingType": "direct"
        },
        "portMode": "unknown",
        "domainNumber": 0,
        "attachedChannelPortRef": "string",
        "discoveryStatus": 0
      },
      "interfaceRef": "string",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "protectionInformationCapable": True,
      "oneWayMaxRate": "string",
      "bidirectionalMaxRate": "string",
      "controllerId": "string",
      "niceAddressId": "string",
      "interfaceId": "string",
      "addressId": "string",
      "basePortAddress": "string",
      "id": "string"
    }
  ],
  "ethernetPorts": [
    {
      "interfaceRef": "string",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "channel": 0,
      "channelPortRef": "string",
      "interfaceData": {
        "type": "unknown",
        "ethernetData": {
          "partData": {
            "vendorName": "string",
            "partNumber": "string",
            "revisionNumber": "string",
            "serialNumber": "string"
          },
          "macAddress": "string",
          "fullDuplex": True,
          "maximumFramePayloadSize": 0,
          "currentInterfaceSpeed": "speedUnknown",
          "maximumInterfaceSpeed": "speedUnknown",
          "linkStatus": "none",
          "supportedInterfaceSpeeds": [
            "speedUnknown"
          ],
          "autoconfigSupport": True,
          "copperCableDiagnosticsSupport": True,
          "operationalInterfaceSpeed": "speedUnknown"
        },
        "infinibandData": {
          "isIser": True
        }
      },
      "protectionInformationCapable": True,
      "oneWayMaxRate": "string",
      "bidirectionalMaxRate": "string",
      "controllerId": "string",
      "commandProtocolProperties": [
        {
          "commandProtocol": "unknown",
          "nvmeProperties": {
            "commandSet": "unknown",
            "nvmeofProperties": {
              "provider": "providerUnknown",
              "ibProperties": {
                "ipAddressData": {
                  "addressType": "ipv4",
                  "ipv4Data": {
                    "configState": "unconfigured",
                    "ipv4Address": "string",
                    "ipv4SubnetMask": "string",
                    "ipv4GatewayAddress": "string"
                  },
                  "ipv6Data": {
                    "address": "string",
                    "addressState": {
                      "addressType": "typeInterface",
                      "interfaceAddressState": "unconfigured",
                      "routerAddressState": "unknown"
                    }
                  }
                },
                "listeningPort": 0
              },
              "roceV2Properties": {
                "ipv4Enabled": True,
                "ipv6Enabled": True,
                "ipv4Data": {
                  "ipv4Address": "string",
                  "ipv4AddressConfigMethod": "configDhcp",
                  "ipv4OutboundPacketPriority": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv4VlanId": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv4AddressData": {
                    "configState": "unconfigured",
                    "ipv4Address": "string",
                    "ipv4SubnetMask": "string",
                    "ipv4GatewayAddress": "string"
                  }
                },
                "ipv6Data": {
                  "ipv6LocalAddresses": [
                    {
                      "address": "string",
                      "addressState": {
                        "addressType": "typeInterface",
                        "interfaceAddressState": "unconfigured",
                        "routerAddressState": "unknown"
                      }
                    }
                  ],
                  "ipv6RoutableAddresses": [
                    {
                      "address": "string",
                      "addressState": {
                        "addressType": "typeInterface",
                        "interfaceAddressState": "unconfigured",
                        "routerAddressState": "unknown"
                      }
                    }
                  ],
                  "ipv6PortRouterAddress": {
                    "address": "string",
                    "addressState": {
                      "addressType": "typeInterface",
                      "interfaceAddressState": "unconfigured",
                      "routerAddressState": "unknown"
                    }
                  },
                  "ipv6AddressConfigMethod": "configStatic",
                  "ipv6OutboundPacketPriority": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv6VlanId": {
                    "isEnabled": True,
                    "value": 0
                  },
                  "ipv6HopLimit": 0,
                  "ipv6NdReachableTime": 0,
                  "ipv6NdRetransmitTime": 0,
                  "ipv6NdStaleTimeout": 0,
                  "ipv6DuplicateAddressDetectionAttempts": 0
                },
                "listeningPort": 0
              },
              "fcProperties": {
                "firstBurstDataSupported": True,
                "firstBurstDataLength": 0
              }
            }
          }
        }
      ],
      "niceAddressId": "string",
      "interfaceId": "string",
      "addressId": "string",
      "id": "string"
    }
  ],
  "sasExpanders": [
    {
      "expanderRef": "string",
      "parent": {
        "expanderParentType": "unknown",
        "parentController": "string",
        "parentEsm": "string",
        "parentDrawer": "string"
      },
      "channel": 0,
      "deviceName": "string",
      "vendorId": "string",
      "productId": "string",
      "fwVersion": "string",
      "expanderPorts": [
        {
          "parent": {
            "type": "controller",
            "controller": "string",
            "drive": "string",
            "expander": "string",
            "hostBoardRef": "string"
          },
          "attachedDevice": {
            "channel": 0,
            "channelType": "hostside",
            "sasAttachedDeviceData": {
              "type": "unknown",
              "alternateController": "string",
              "drive": "string",
              "expander": "string",
              "remoteHostPortAddress": "string",
              "localController": "string",
              "physicalLocation": {
                "trayRef": "string",
                "slot": 0,
                "locationParent": {
                  "refType": "generic",
                  "controllerRef": "string",
                  "symbolRef": "string",
                  "typedReference": {
                    "componentType": "unknown",
                    "symbolRef": "string"
                  }
                },
                "locationPosition": 0,
                "label": "string"
              }
            }
          },
          "state": "unknown",
          "miswireType": "none",
          "channelPortRef": "string",
          "sasPhys": [
            {
              "phyIdentifier": 0,
              "isOperational": True
            }
          ],
          "portTypeData": {
            "portType": "endDevice",
            "portIdentifier": "string",
            "routingType": "direct"
          },
          "portMode": "unknown",
          "domainNumber": 0,
          "attachedChannelPortRef": "string",
          "discoveryStatus": 0
        }
      ],
      "domainNumber": 0,
      "id": "string"
    }
  ],
  "channelPorts": [
    {
      "portRef": "string",
      "portParent": {
        "type": "unknown",
        "controllerRef": "string",
        "esmRef": "string",
        "minihubRef": "string",
        "hicRef": "string"
      },
      "portNumber": 0,
      "channel": 0,
      "channelType": "hostside",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "isTrunkActive": True,
      "id": "string"
    }
  ],
  "trays": [
    {
      "type": "sym1000",
      "orientation": "horizontal",
      "numControllerSlots": 0,
      "numDriveSlots": 0,
      "trayId": 0,
      "trayRef": "string",
      "nonRedundantAccess": True,
      "partNumber": "string",
      "serialNumber": "string",
      "vendorName": "string",
      "manufacturerDate": "string",
      "fruType": "string",
      "trayIDMismatch": True,
      "trayIDConflict": True,
      "esmVersionMismatch": True,
      "esmMiswire": True,
      "drvMHSpeedMismatch": True,
      "unsupportedTray": True,
      "workingChannel": 0,
      "maxSpeed": "speedUnknown",
      "trayTechnologyType": "unknown",
      "esmGroupError": True,
      "uncertifiedTray": True,
      "locateTray": True,
      "esmHardwareMismatch": True,
      "hasConfigurableTrayId": True,
      "frontEndInterfaceTechnology": "notImplemented",
      "driveTechnologies": [
        "all"
      ],
      "numDriveCompartments": 0,
      "numDriveSlotsPerCompartment": 0,
      "trayAttributes": [
        {
          "attributeId": "assetTag",
          "attributeValue": "string"
        }
      ],
      "isMisconfigured": True,
      "esmFactoryDefaultsMismatch": True,
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "numDrawers": 0,
      "driveLayout": {
        "driveOrientation": "none",
        "numRows": 0,
        "numColumns": 0,
        "primaryTraversal": "none",
        "secondaryTraversal": "none"
      },
      "factoryDefaultsData": {
        "factoryDefaultsVersion": "string",
        "isSupported": True
      },
      "locateInProgress": True,
      "hasTrayIdentityIndicator": True,
      "oemPartNumber": "string",
      "trayPositionIndex": 0,
      "id": "string"
    }
  ],
  "drawers": [
    {
      "drawerRef": "string",
      "isOpen": True,
      "status": "unknown",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "softwareVersion": "string",
      "partNumber": "string",
      "serialNumber": "string",
      "vendorName": "string",
      "manufactureDate": "string",
      "fruType": "string",
      "drawerType": "string",
      "id": "string"
    }
  ],
  "controllers": [
    {
      "active": True,
      "quiesced": True,
      "status": "unknown",
      "controllerRef": "string",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "manufacturer": "string",
      "manufacturerDate": "string",
      "appVersion": "string",
      "bootVersion": "string",
      "productID": "string",
      "productRevLevel": "string",
      "serialNumber": "string",
      "boardID": "string",
      "cacheMemorySize": 0,
      "processorMemorySize": 0,
      "hostInterfaces": [
        {
          "interfaceType": "notImplemented",
          "fibre": {
            "channel": 0,
            "loopID": 0,
            "speed": 0,
            "hardAddress": 0,
            "nodeName": "string",
            "portName": "string",
            "portId": "string",
            "topology": "unknown",
            "part": "string",
            "revision": 0,
            "chanMiswire": True,
            "esmMiswire": True,
            "linkStatus": "none",
            "isDegraded": True,
            "speedControl": "unknown",
            "maxSpeed": 0,
            "speedNegError": True,
            "reserved1": "string",
            "reserved2": "string",
            "ddsChannelState": 0,
            "ddsStateReason": 0,
            "ddsStateWho": 0,
            "isLocal": True,
            "channelPorts": [
              {
                "speedDetError": True,
                "manuallyBypassed": True,
                "portNumber": "portUnknown"
              }
            ],
            "currentInterfaceSpeed": "speedUnknown",
            "maximumInterfaceSpeed": "speedUnknown",
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "isTrunkCapable": True,
            "trunkMiswire": True,
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "fc4Types": [
              "common"
            ],
            "id": "string"
          },
          "ib": {
            "interfaceRef": "string",
            "channel": 0,
            "channelPortRef": "string",
            "localIdentifier": 0,
            "globalIdentifier": "string",
            "linkState": "initialize",
            "portState": "unknown",
            "maximumTransmissionUnit": 0,
            "currentSpeed": "speedUnknown",
            "supportedSpeed": [
              "speedUnknown"
            ],
            "currentLinkWidth": "width1x",
            "supportedLinkWidth": [
              "width1x"
            ],
            "currentDataVirtualLanes": 0,
            "maximumDataVirtualLanes": 0,
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "isSRPSupported": True,
            "isISERSupported": True,
            "physPortState": "unknown",
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "isNVMeSupported": True,
            "id": "string"
          },
          "iscsi": {
            "channel": 0,
            "channelPortRef": "string",
            "tcpListenPort": 0,
            "ipv4Enabled": True,
            "ipv4Data": {
              "ipv4Address": "string",
              "ipv4AddressConfigMethod": "configDhcp",
              "ipv4OutboundPacketPriority": {
                "isEnabled": True,
                "value": 0
              },
              "ipv4VlanId": {
                "isEnabled": True,
                "value": 0
              },
              "ipv4AddressData": {
                "configState": "unconfigured",
                "ipv4Address": "string",
                "ipv4SubnetMask": "string",
                "ipv4GatewayAddress": "string"
              }
            },
            "interfaceData": {
              "type": "unknown",
              "ethernetData": {
                "partData": {
                  "vendorName": "string",
                  "partNumber": "string",
                  "revisionNumber": "string",
                  "serialNumber": "string"
                },
                "macAddress": "string",
                "fullDuplex": True,
                "maximumFramePayloadSize": 0,
                "currentInterfaceSpeed": "speedUnknown",
                "maximumInterfaceSpeed": "speedUnknown",
                "linkStatus": "none",
                "supportedInterfaceSpeeds": [
                  "speedUnknown"
                ],
                "autoconfigSupport": True,
                "copperCableDiagnosticsSupport": True,
                "operationalInterfaceSpeed": "speedUnknown"
              },
              "infinibandData": {
                "isIser": True
              }
            },
            "interfaceRef": "string",
            "ipv6Enabled": True,
            "ipv6Data": {
              "ipv6LocalAddresses": [
                {
                  "address": "string",
                  "addressState": {
                    "addressType": "typeInterface",
                    "interfaceAddressState": "unconfigured",
                    "routerAddressState": "unknown"
                  }
                }
              ],
              "ipv6RoutableAddresses": [
                {
                  "address": "string",
                  "addressState": {
                    "addressType": "typeInterface",
                    "interfaceAddressState": "unconfigured",
                    "routerAddressState": "unknown"
                  }
                }
              ],
              "ipv6PortRouterAddress": {
                "address": "string",
                "addressState": {
                  "addressType": "typeInterface",
                  "interfaceAddressState": "unconfigured",
                  "routerAddressState": "unknown"
                }
              },
              "ipv6AddressConfigMethod": "configStatic",
              "ipv6OutboundPacketPriority": {
                "isEnabled": True,
                "value": 0
              },
              "ipv6VlanId": {
                "isEnabled": True,
                "value": 0
              },
              "ipv6HopLimit": 0,
              "ipv6NdReachableTime": 0,
              "ipv6NdRetransmitTime": 0,
              "ipv6NdStaleTimeout": 0,
              "ipv6DuplicateAddressDetectionAttempts": 0
            },
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "isIPv6Capable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "id": "string"
          },
          "sas": {
            "channel": 0,
            "currentInterfaceSpeed": "speedUnknown",
            "maximumInterfaceSpeed": "speedUnknown",
            "part": "string",
            "revision": 0,
            "isDegraded": True,
            "iocPort": {
              "parent": {
                "type": "controller",
                "controller": "string",
                "drive": "string",
                "expander": "string",
                "hostBoardRef": "string"
              },
              "attachedDevice": {
                "channel": 0,
                "channelType": "hostside",
                "sasAttachedDeviceData": {
                  "type": "unknown",
                  "alternateController": "string",
                  "drive": "string",
                  "expander": "string",
                  "remoteHostPortAddress": "string",
                  "localController": "string",
                  "physicalLocation": {
                    "trayRef": "string",
                    "slot": 0,
                    "locationParent": {
                      "refType": "generic",
                      "controllerRef": "string",
                      "symbolRef": "string",
                      "typedReference": {
                        "componentType": "unknown",
                        "symbolRef": "string"
                      }
                    },
                    "locationPosition": 0,
                    "label": "string"
                  }
                }
              },
              "state": "unknown",
              "miswireType": "none",
              "channelPortRef": "string",
              "sasPhys": [
                {
                  "phyIdentifier": 0,
                  "isOperational": True
                }
              ],
              "portTypeData": {
                "portType": "endDevice",
                "portIdentifier": "string",
                "routingType": "direct"
              },
              "portMode": "unknown",
              "domainNumber": 0,
              "attachedChannelPortRef": "string",
              "discoveryStatus": 0
            },
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "id": "string"
          },
          "sata": {
            "channel": 0,
            "currentInterfaceSpeed": "speedUnknown",
            "maximumInterfaceSpeed": "speedUnknown",
            "speedControl": "unknown",
            "part": "string",
            "revision": 0,
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "id": "string"
          },
          "scsi": {
            "channel": 0,
            "scsiID": 0,
            "speed": 0,
            "scsiType": "se",
            "width": 0,
            "part": "string",
            "revision": 0,
            "reserved1": "string",
            "reserved2": "string"
          },
          "couplingDriverNvme": {
            "interfaceRef": "string",
            "channel": 0,
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string"
          },
          "ethernet": {
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "channel": 0,
            "channelPortRef": "string",
            "interfaceData": {
              "type": "unknown",
              "ethernetData": {
                "partData": {
                  "vendorName": "string",
                  "partNumber": "string",
                  "revisionNumber": "string",
                  "serialNumber": "string"
                },
                "macAddress": "string",
                "fullDuplex": True,
                "maximumFramePayloadSize": 0,
                "currentInterfaceSpeed": "speedUnknown",
                "maximumInterfaceSpeed": "speedUnknown",
                "linkStatus": "none",
                "supportedInterfaceSpeeds": [
                  "speedUnknown"
                ],
                "autoconfigSupport": True,
                "copperCableDiagnosticsSupport": True,
                "operationalInterfaceSpeed": "speedUnknown"
              },
              "infinibandData": {
                "isIser": True
              }
            },
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "id": "string"
          }
        }
      ],
      "driveInterfaces": [
        {
          "interfaceType": "notImplemented",
          "fibre": {
            "channel": 0,
            "loopID": 0,
            "speed": 0,
            "hardAddress": 0,
            "nodeName": "string",
            "portName": "string",
            "portId": "string",
            "topology": "unknown",
            "part": "string",
            "revision": 0,
            "chanMiswire": True,
            "esmMiswire": True,
            "linkStatus": "none",
            "isDegraded": True,
            "speedControl": "unknown",
            "maxSpeed": 0,
            "speedNegError": True,
            "reserved1": "string",
            "reserved2": "string",
            "ddsChannelState": 0,
            "ddsStateReason": 0,
            "ddsStateWho": 0,
            "isLocal": True,
            "channelPorts": [
              {
                "speedDetError": True,
                "manuallyBypassed": True,
                "portNumber": "portUnknown"
              }
            ],
            "currentInterfaceSpeed": "speedUnknown",
            "maximumInterfaceSpeed": "speedUnknown",
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "isTrunkCapable": True,
            "trunkMiswire": True,
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "fc4Types": [
              "common"
            ],
            "id": "string"
          },
          "ib": {
            "interfaceRef": "string",
            "channel": 0,
            "channelPortRef": "string",
            "localIdentifier": 0,
            "globalIdentifier": "string",
            "linkState": "initialize",
            "portState": "unknown",
            "maximumTransmissionUnit": 0,
            "currentSpeed": "speedUnknown",
            "supportedSpeed": [
              "speedUnknown"
            ],
            "currentLinkWidth": "width1x",
            "supportedLinkWidth": [
              "width1x"
            ],
            "currentDataVirtualLanes": 0,
            "maximumDataVirtualLanes": 0,
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "isSRPSupported": True,
            "isISERSupported": True,
            "physPortState": "unknown",
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "isNVMeSupported": True,
            "id": "string"
          },
          "iscsi": {
            "channel": 0,
            "channelPortRef": "string",
            "tcpListenPort": 0,
            "ipv4Enabled": True,
            "ipv4Data": {
              "ipv4Address": "string",
              "ipv4AddressConfigMethod": "configDhcp",
              "ipv4OutboundPacketPriority": {
                "isEnabled": True,
                "value": 0
              },
              "ipv4VlanId": {
                "isEnabled": True,
                "value": 0
              },
              "ipv4AddressData": {
                "configState": "unconfigured",
                "ipv4Address": "string",
                "ipv4SubnetMask": "string",
                "ipv4GatewayAddress": "string"
              }
            },
            "interfaceData": {
              "type": "unknown",
              "ethernetData": {
                "partData": {
                  "vendorName": "string",
                  "partNumber": "string",
                  "revisionNumber": "string",
                  "serialNumber": "string"
                },
                "macAddress": "string",
                "fullDuplex": True,
                "maximumFramePayloadSize": 0,
                "currentInterfaceSpeed": "speedUnknown",
                "maximumInterfaceSpeed": "speedUnknown",
                "linkStatus": "none",
                "supportedInterfaceSpeeds": [
                  "speedUnknown"
                ],
                "autoconfigSupport": True,
                "copperCableDiagnosticsSupport": True,
                "operationalInterfaceSpeed": "speedUnknown"
              },
              "infinibandData": {
                "isIser": True
              }
            },
            "interfaceRef": "string",
            "ipv6Enabled": True,
            "ipv6Data": {
              "ipv6LocalAddresses": [
                {
                  "address": "string",
                  "addressState": {
                    "addressType": "typeInterface",
                    "interfaceAddressState": "unconfigured",
                    "routerAddressState": "unknown"
                  }
                }
              ],
              "ipv6RoutableAddresses": [
                {
                  "address": "string",
                  "addressState": {
                    "addressType": "typeInterface",
                    "interfaceAddressState": "unconfigured",
                    "routerAddressState": "unknown"
                  }
                }
              ],
              "ipv6PortRouterAddress": {
                "address": "string",
                "addressState": {
                  "addressType": "typeInterface",
                  "interfaceAddressState": "unconfigured",
                  "routerAddressState": "unknown"
                }
              },
              "ipv6AddressConfigMethod": "configStatic",
              "ipv6OutboundPacketPriority": {
                "isEnabled": True,
                "value": 0
              },
              "ipv6VlanId": {
                "isEnabled": True,
                "value": 0
              },
              "ipv6HopLimit": 0,
              "ipv6NdReachableTime": 0,
              "ipv6NdRetransmitTime": 0,
              "ipv6NdStaleTimeout": 0,
              "ipv6DuplicateAddressDetectionAttempts": 0
            },
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "isIPv6Capable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "id": "string"
          },
          "sas": {
            "channel": 0,
            "currentInterfaceSpeed": "speedUnknown",
            "maximumInterfaceSpeed": "speedUnknown",
            "part": "string",
            "revision": 0,
            "isDegraded": True,
            "iocPort": {
              "parent": {
                "type": "controller",
                "controller": "string",
                "drive": "string",
                "expander": "string",
                "hostBoardRef": "string"
              },
              "attachedDevice": {
                "channel": 0,
                "channelType": "hostside",
                "sasAttachedDeviceData": {
                  "type": "unknown",
                  "alternateController": "string",
                  "drive": "string",
                  "expander": "string",
                  "remoteHostPortAddress": "string",
                  "localController": "string",
                  "physicalLocation": {
                    "trayRef": "string",
                    "slot": 0,
                    "locationParent": {
                      "refType": "generic",
                      "controllerRef": "string",
                      "symbolRef": "string",
                      "typedReference": {
                        "componentType": "unknown",
                        "symbolRef": "string"
                      }
                    },
                    "locationPosition": 0,
                    "label": "string"
                  }
                }
              },
              "state": "unknown",
              "miswireType": "none",
              "channelPortRef": "string",
              "sasPhys": [
                {
                  "phyIdentifier": 0,
                  "isOperational": True
                }
              ],
              "portTypeData": {
                "portType": "endDevice",
                "portIdentifier": "string",
                "routingType": "direct"
              },
              "portMode": "unknown",
              "domainNumber": 0,
              "attachedChannelPortRef": "string",
              "discoveryStatus": 0
            },
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "id": "string"
          },
          "sata": {
            "channel": 0,
            "currentInterfaceSpeed": "speedUnknown",
            "maximumInterfaceSpeed": "speedUnknown",
            "speedControl": "unknown",
            "part": "string",
            "revision": 0,
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "id": "string"
          },
          "scsi": {
            "channel": 0,
            "scsiID": 0,
            "speed": 0,
            "scsiType": "se",
            "width": 0,
            "part": "string",
            "revision": 0,
            "reserved1": "string",
            "reserved2": "string"
          },
          "couplingDriverNvme": {
            "interfaceRef": "string",
            "channel": 0,
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string"
          },
          "ethernet": {
            "interfaceRef": "string",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            },
            "channel": 0,
            "channelPortRef": "string",
            "interfaceData": {
              "type": "unknown",
              "ethernetData": {
                "partData": {
                  "vendorName": "string",
                  "partNumber": "string",
                  "revisionNumber": "string",
                  "serialNumber": "string"
                },
                "macAddress": "string",
                "fullDuplex": True,
                "maximumFramePayloadSize": 0,
                "currentInterfaceSpeed": "speedUnknown",
                "maximumInterfaceSpeed": "speedUnknown",
                "linkStatus": "none",
                "supportedInterfaceSpeeds": [
                  "speedUnknown"
                ],
                "autoconfigSupport": True,
                "copperCableDiagnosticsSupport": True,
                "operationalInterfaceSpeed": "speedUnknown"
              },
              "infinibandData": {
                "isIser": True
              }
            },
            "protectionInformationCapable": True,
            "oneWayMaxRate": "string",
            "bidirectionalMaxRate": "string",
            "id": "string"
          }
        }
      ],
      "netInterfaces": [
        {
          "interfaceType": "ethernet",
          "ethernet": {
            "interfaceName": "string",
            "channel": 0,
            "speed": 0,
            "ip": 0,
            "alias": "string",
            "macAddr": "string",
            "gatewayIp": 0,
            "subnetMask": 0,
            "bootpUsed": True,
            "rloginEnabled": True,
            "reserved1": "string",
            "setupError": True,
            "reserved2": "string",
            "interfaceRef": "string",
            "linkStatus": "none",
            "ipv4Enabled": True,
            "ipv4Address": "string",
            "ipv4SubnetMask": "string",
            "ipv4AddressConfigMethod": "configDhcp",
            "ipv6Enabled": True,
            "ipv6LocalAddress": {
              "address": "string",
              "addressState": {
                "addressType": "typeInterface",
                "interfaceAddressState": "unconfigured",
                "routerAddressState": "unknown"
              }
            },
            "ipv6PortStaticRoutableAddress": {
              "address": "string",
              "addressState": {
                "addressType": "typeInterface",
                "interfaceAddressState": "unconfigured",
                "routerAddressState": "unknown"
              }
            },
            "ipv6PortRoutableAddresses": [
              {
                "address": "string",
                "addressState": {
                  "addressType": "typeInterface",
                  "interfaceAddressState": "unconfigured",
                  "routerAddressState": "unknown"
                }
              }
            ],
            "ipv6AddressConfigMethod": "configStatic",
            "fullDuplex": True,
            "supportedSpeedSettings": [
              "speedNone"
            ],
            "configuredSpeedSetting": "speedNone",
            "currentSpeed": "speedUnknown",
            "physicalLocation": {
              "trayRef": "string",
              "slot": 0,
              "locationParent": {
                "refType": "generic",
                "controllerRef": "string",
                "symbolRef": "string",
                "typedReference": {
                  "componentType": "unknown",
                  "symbolRef": "string"
                }
              },
              "locationPosition": 0,
              "label": "string"
            }
          }
        }
      ],
      "inventory": [
        {
          "itemName": "string",
          "itemVersion": "string"
        }
      ],
      "reserved1": "string",
      "reserved2": "string",
      "hostBoardID": "string",
      "physicalCacheMemorySize": 0,
      "readyToRemove": True,
      "boardSubmodelID": "string",
      "submodelSupported": True,
      "oemPartNumber": "string",
      "partNumber": "string",
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "bootTime": "string",
      "modelName": "string",
      "networkSettings": {
        "ipv4DefaultRouterAddress": "string",
        "ipv6DefaultRouterAddress": {
          "address": "string",
          "addressState": {
            "addressType": "typeInterface",
            "interfaceAddressState": "unconfigured",
            "routerAddressState": "unknown"
          }
        },
        "ipv6CandidateDefaultRouterAddresses": [
          {
            "address": "string",
            "addressState": {
              "addressType": "typeInterface",
              "interfaceAddressState": "unconfigured",
              "routerAddressState": "unknown"
            }
          }
        ],
        "remoteAccessEnabled": True,
        "dnsProperties": {
          "acquisitionProperties": {
            "dnsAcquisitionType": "unknown",
            "dnsServers": [
              {
                "addressType": "ipv4",
                "ipv4Address": "string",
                "ipv6Address": "string"
              }
            ]
          },
          "dhcpAcquiredDnsServers": [
            {
              "addressType": "ipv4",
              "ipv4Address": "string",
              "ipv6Address": "string"
            }
          ]
        },
        "ntpProperties": {
          "acquisitionProperties": {
            "ntpAcquisitionType": "unknown",
            "ntpServers": [
              {
                "addrType": "none",
                "domainName": "string",
                "ipvxAddress": {
                  "addressType": "ipv4",
                  "ipv4Address": "string",
                  "ipv6Address": "string"
                }
              }
            ]
          },
          "dhcpAcquiredNtpServers": [
            {
              "addressType": "ipv4",
              "ipv4Address": "string",
              "ipv6Address": "string"
            }
          ]
        }
      },
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "flashCacheMemorySize": 0,
      "ctrlIocDumpData": {
        "iocDumpNeedsRetrieved": True,
        "iocDumpTag": 0,
        "timeStamp": "string"
      },
      "locateInProgress": True,
      "hasTrayIdentityIndicator": True,
      "controllerErrorMode": "notInErrorMode",
      "codeVersions": [
        {
          "codeModule": "unspecified",
          "versionString": "string"
        }
      ],
      "id": "string"
    }
  ],
  "batteries": [
    {
      "batteryRef": "string",
      "status": "optimal",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "batteryAge": 0,
      "batteryLifeRemaining": 0,
      "batteryTypeData": {
        "batteryType": "singleSharedCru",
        "cruParentController": "string",
        "parentController": "string"
      },
      "reserved1": "string",
      "reserved2": "string",
      "manufacturerDate": "string",
      "vendorName": "string",
      "vendorPN": "string",
      "vendorSN": "string",
      "fruType": "string",
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "batteryCanExpire": True,
      "automaticAgeReset": True,
      "learnCycleData": {
        "lastBatteryLearnCycle": "string",
        "nextBatteryLearnCycle": "string",
        "batteryLearnCycleInterval": 0
      },
      "smartBatteryData": {
        "lastBatteryLearnCycle": "string",
        "nextBatteryLearnCycle": "string",
        "batteryLearnCycleInterval": 0
      },
      "id": "string"
    }
  ],
  "fans": [
    {
      "fanRef": "string",
      "status": "optimal",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "reserved1": "string",
      "reserved2": "string",
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "id": "string"
    }
  ],
  "hostBoards": [
    {
      "parentController": "string",
      "partNumber": "string",
      "serialNumber": "string",
      "vendorName": "string",
      "manufacturerDate": "string",
      "fruType": "string",
      "hostBoardId": "string",
      "status": "unknown",
      "type": "typeUnknown",
      "hostBoardRef": "string",
      "numberOfPorts": 0,
      "hbTypeData": {
        "type": "typeUnknown",
        "dualPortIbTypeData": {
          "tcaGuid": "string",
          "queuePairsSupported": 0,
          "completionQueuesSupported": 0,
          "sharedReceiveQueuesSupported": 0
        },
        "dualPortDenaliIbTypeData": {
          "tcaGuid": "string",
          "queuePairsSupported": 0,
          "completionQueuesSupported": 0,
          "sharedReceiveQueuesSupported": 0
        }
      },
      "oemPartNumber": "string",
      "hostBoardControllerSlot": 0,
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "id": "string"
    }
  ],
  "powerSupplies": [
    {
      "powerSupplyRef": "string",
      "status": "optimal",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "partNumber": "string",
      "serialNumber": "string",
      "vendorName": "string",
      "manufacturerDate": "string",
      "fruType": "string",
      "reserved1": "string",
      "reserved2": "string",
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "firmwareRevision": "string",
      "manufacturingDeviceCode": 0,
      "id": "string"
    }
  ],
  "nvsramVersion": "string",
  "cacheMemoryDimms": [
    {
      "cacheMemoryDimmRef": "string",
      "status": "unknown",
      "capacityInMegabytes": 0,
      "serialNumber": "string",
      "partNumber": "string",
      "oemPartNumber": "string",
      "manufacturerPartNumber": "string",
      "manufacturer": "string",
      "manufactureDate": "string",
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "shared": True,
      "revisionCode": "string"
    }
  ],
  "cacheBackupDevices": [
    {
      "backupDeviceRef": "string",
      "backupDeviceControllerSlot": 0,
      "parentController": "string",
      "backupDeviceType": "unknown",
      "backupDeviceStatus": "unknown",
      "backupDeviceVpd": {
        "manufacturer": "string",
        "manufactureDate": "string",
        "productId": "string",
        "productRevLevel": "string",
        "partNumber": "string",
        "serialNumber": "string"
      },
      "backupDeviceCapacity": 0,
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "id": "string"
    }
  ],
  "supportCRUs": [
    {
      "supportCRURef": "string",
      "status": "unknown",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "manufacturerDate": "string",
      "vendorName": "string",
      "vendorPN": "string",
      "vendorSN": "string",
      "fruType": "string",
      "readyToRemove": True,
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "configuredComponents": [
        "unknown"
      ],
      "type": "unknown",
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "id": "string"
    }
  ],
  "esms": [
    {
      "esmRef": "string",
      "status": "optimal",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "nonRedundantAccess": True,
      "partNumber": "string",
      "serialNumber": "string",
      "manufacturerDate": "string",
      "manufacturer": "string",
      "fruType": "string",
      "softwareVersion": "string",
      "esmInterfaceData": {
        "ioInterfaceType": "notImplemented",
        "portList": {
          "ports": [
            {
              "portStatus": "bypassed",
              "portType": "gbic",
              "reserved1": "string",
              "reserved2": "string"
            }
          ]
        }
      },
      "productID": "string",
      "workingChannel": 0,
      "currentSpeed": "speedUnknown",
      "maxSpeed": "speedUnknown",
      "reserved1": "string",
      "reserved2": "string",
      "fibreEsm": {
        "esmPortRef": "string",
        "loopID": 0,
        "portRef": "string"
      },
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "esmInterfaceAttributes": {
        "ioInterfaceType": "notImplemented",
        "fibreEsmAttributes": {
          "isSwitched": True,
          "fibreEsmAddress": {
            "esmPortRef": "string",
            "loopID": 0,
            "portRef": "string"
          }
        },
        "sasEsmAttributes": {
          "sasExpander": [
            "string"
          ]
        }
      },
      "boardId": "string",
      "factoryDefaultsData": {
        "isSupported": True,
        "factoryDefaultsVersion": "string"
      },
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "isTrunkCapable": True,
      "trunkMiswire": True,
      "locateInProgress": True,
      "hasTrayIdentityIndicator": True,
      "esmType": "unidentified",
      "id": "string"
    }
  ],
  "sfps": [
    {
      "sfpRef": "string",
      "status": "optimal",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "sfpType": {
        "sfpIdentType": "unknown",
        "sfpConnectType": "unknown",
        "sfpLinkLType": "typeUnknown",
        "sfpTransmitterType": "unknown",
        "sfpSpeed": [
          "typeUnknown"
        ],
        "sfpTransmissionMedia": [
          "unknown"
        ],
        "manufacturerDate": "string",
        "vendorName": "string",
        "vendorPN": "string",
        "vendorRev": "string",
        "vendorSN": "string",
        "vendorOUI": "string",
        "reserved1": "string",
        "reserved2": "string"
      },
      "sfpPort": "portUnknown",
      "parentData": {
        "sfpParentType": "unknown",
        "controllerSFP": {
          "controllerSFPType": "hostside",
          "parentController": "string",
          "channel": 0,
          "reserved1": "string",
          "reserved2": "string"
        },
        "parentEsm": "string",
        "parentMinihub": "string"
      },
      "reserved1": "string",
      "reserved2": "string",
      "sfpPortRef": "string",
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "id": "string"
    }
  ],
  "thermalSensors": [
    {
      "thermalSensorRef": "string",
      "status": "optimal",
      "physicalLocation": {
        "trayRef": "string",
        "slot": 0,
        "locationParent": {
          "refType": "generic",
          "controllerRef": "string",
          "symbolRef": "string",
          "typedReference": {
            "componentType": "unknown",
            "symbolRef": "string"
          }
        },
        "locationPosition": 0,
        "label": "string"
      },
      "reserved1": "string",
      "reserved2": "string",
      "rtrAttributes": {
        "cruType": "unknown",
        "parentCru": {
          "type": "controller",
          "parentController": "string",
          "parentEsm": "string",
          "parentFan": "string",
          "parentInterconnectCru": "string",
          "parentSupportCru": "string",
          "parentDrawer": "string"
        },
        "rtrAttributeData": {
          "hasReadyToRemoveIndicator": True,
          "readyToRemove": True
        }
      },
      "repairPolicy": {
        "removalData": {
          "removalMethod": "parent",
          "rtrAttributes": {
            "hasReadyToRemoveIndicator": True,
            "readyToRemove": True
          }
        },
        "replacementMethod": "parent"
      },
      "id": "string"
    }
  ]
}

valid_config_data = {
    "username": "admin",
    "password": "admin"
}

class TestCollector(unittest.TestCase):

    @patch("collector.requests.Session")
    def test_get_drive_location(self, mock_session):
        sys_id = "0"
        req_url = ("{}/{}/hardware-inventory").format(collector.PROXY_BASE_URL, sys_id)
        
        mock_session.get.json.return_value = json_response

        drive_loc = collector.get_drive_location(sys_id, mock_session)
        mock_session.get.assert_called_with(req_url)

    @patch("collector.requests")
    @patch("collector.json")
    def test_get_session_valid_config(self, mock_json_load, mock_requests):
        mock_json_load.return_value = valid_config_data
        with patch("collector.open", mock_open()):
            try:
                collector.get_session()
            except:
                self.fail("get_session raised an exception with valid config data")

    @patch("collector.requests")
    @patch("collector.json")
    @patch("collector.CMD")
    @patch("collector.LOG")
    def test_get_session_invalid_config(self, mock_log, mock_cmd, mock_json_load, mock_requests):
        mock_json_load.return_value = valid_config_data
        mock_cmd.username = ""
        mock_cmd.password = ""
        with patch("collector.open", mock_open()) as mocked_open:
            mocked_open.side_effect = IOError
            collector.get_session()
            mock_log.exception.assert_called()
