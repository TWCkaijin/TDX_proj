import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';
import 'package:gdsc/firebase_options.dart';
import 'dart:developer';

class MapPage extends StatefulWidget {
  const MapPage({super.key});

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  LatLng _BeginPosition = LatLng(22.632820, 120.300487);
  Location _LocationController = new Location();
  LatLng? _currentPositon = null;
  late GoogleMapController mapController;

  void _onMapCreated(GoogleMapController controller) {
    mapController = controller;
  }

  @override
  void initState() {
    super.initState();
    getLocationUpdates();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        home: Scaffold(
          
          body: Stack(
            children: <Widget>[
               _currentPositon == null
          ? const Center(child: Text("Loading..."))
          : GoogleMap(
                onMapCreated: _onMapCreated,
                initialCameraPosition: CameraPosition(
                  target: _BeginPosition,
                  zoom: 12.5,
                ),
                markers: {
                  Marker(
                    markerId: MarkerId("_currentPositon"),
                    icon: BitmapDescriptor.defaultMarker,
                    position: _currentPositon!,
                  )
                },
                myLocationButtonEnabled: false,
                zoomControlsEnabled: false,
              ),
              DraggableScrollableSheet(
                initialChildSize: 0.3,
                minChildSize: 0.05,
                maxChildSize: 0.9,
                builder:
                    (BuildContext context, ScrollController scrollController) {
                  return Container(
                    decoration: BoxDecoration(
                      color: Colors.blue[100],
                      // remove or decrease the borderRadius
                      borderRadius: const BorderRadius.vertical(
                          top: Radius.circular(20.0)),
                    ),
                    child: ListView.builder(
                      controller: scrollController,
                      itemCount: 25,
                      itemBuilder: (BuildContext context, int index) {
                        return ListTile(title: Text('Item $index'));
                      },
                      padding: EdgeInsets.zero,
                    ),
                  );
                },
              ),
            ],
          ),
        ));
  }

  Future<void> getLocationUpdates() async {
    bool _service_Enable;
    PermissionStatus _permissionGranted;

    _service_Enable = await _LocationController.serviceEnabled();

    if (_service_Enable) {
      _service_Enable = await _LocationController.requestService();
    } else {
      return;
    }

    _permissionGranted = await _LocationController.hasPermission();
    if (_permissionGranted == PermissionStatus.denied) {
      _permissionGranted = await _LocationController.requestPermission();
      if (_permissionGranted != PermissionStatus.granted) {
        return;
      }
    }

    _LocationController.onLocationChanged
        .listen((LocationData currentLocation) {
      if (currentLocation.latitude != null &&
          currentLocation.longitude != null) {
        setState(() {
          _currentPositon =
              LatLng(currentLocation.latitude!, currentLocation.longitude!);
          //_currentPositon =LatLng(22.632820, 120.300487);
        });
      }
      log("current_pos : $_currentPositon");
    });
  }
}



