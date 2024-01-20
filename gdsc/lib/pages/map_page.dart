import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';

class MapPage extends StatefulWidget {
  const MapPage({super.key});

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  LatLng _BeginPosition = LatLng(22.632820, 120.300487);
  Location _LocationController = new Location();
  LatLng? _currentPositon = null;

  @override
  void initState() {
    super.initState();
    getLocationUpdates();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _currentPositon == null 
      ? const Center(child: Text("Loading...")) 
      : GoogleMap(initialCameraPosition:CameraPosition(target: _BeginPosition, zoom: 13),
      markers: {
        Marker(
          markerId: MarkerId("_currentPositon"),
          icon: BitmapDescriptor.defaultMarker,
          position: _currentPositon!,
        )
      }

      ),
    );
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

    _LocationController.onLocationChanged.listen((LocationData currentLocation) {
      if (currentLocation.latitude != null &&
          currentLocation.longitude != null) {
        setState(() {
          _currentPositon =LatLng(currentLocation.latitude!, currentLocation.longitude!);
          //_currentPositon =LatLng(22.632820, 120.300487);
          print(_currentPositon);
        });
      }
    });
  }
}
