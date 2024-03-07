import 'dart:async';
import 'dart:developer' as dev;
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:flutter/services.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:location/location.dart';

const LatLng _center = LatLng(22.6239974, 120.2981408);
//TODO:
// 1. Ontap for markers
// 2. Implement pages for settings, bug report, about
// 3. Splash screen or solve the loading issue again

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    name: "potent-result-406711",
    options: DefaultFirebaseOptions.currentPlatform,
  );
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
  ));
  runApp(const MyApp());
}

class ParkingStation extends StatelessWidget {
  final String stationName;
  final int availableLots;
  final LatLng? location;
  final String? pricing;
  final double distance;
  final Function(LatLng) onTap;

  const ParkingStation(
      {super.key,
      required this.stationName,
      required this.availableLots,
      required this.location,
      required this.pricing,
      required this.distance,
      required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
        onTap: () => onTap(location!),
        child: Card(
          elevation: 0.0,
          color: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20.0),
            side: BorderSide(
              color: availableLots > 0
                  ? (availableLots > 10 ? Colors.green : Colors.yellow)
                  : Colors.red,
              width: 2.0,
            ),
          ),
          child: Stack(
            children: <Widget>[
              ListTile(
                title: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    Flexible(child: Text(stationName)),
                    Text(
                        '${availableLots == -1 ? "No info" : "$availableLots spaces"} '),
                  ],
                ),
                subtitle: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    Flexible(child: Text('${distance.toStringAsFixed(2)} km')),
                    Flexible(child: Text('$pricing')),
                  ],
                ),
              ),
            ],
          ),
        ));
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State createState() => _MyAppState();

  // This widget is the root of your application.
}

String formattedDateTime() {
  DateTime now = DateTime.now().subtract(const Duration(minutes: 2));
  int dayOfWeek = now.weekday;
  int timeInMinutes = now.hour * 60 + now.minute;
  int choppedTime = (timeInMinutes * 48) ~/ (24 * 60);
  String formattedDateTime = '$dayOfWeek-$choppedTime';
  return formattedDateTime;
}

class _MyAppState extends State {
  late GoogleMapController mapController;
  bool _showAppBar = true;
  //final LatLng _center = const LatLng(22.6239974, 120.2981408);
  List<ParkingStation> parkingStations = [];
  final Completer<List<ParkingStation>> _completer = Completer();
  final locationController = Location();
  LatLng? _currentPositon;

  String? _mapStyle;
  @override
  void initState() {
    super.initState();
    getLocationUpdates();
    rootBundle.loadString('assets/mapstyle.txt').then((string) {
      _mapStyle = string;
    });
    readDatabase();
  }

  double calculateDistance(lat1, lon1, lat2, lon2) {
    var p = 0.017453292519943295;
    var c = cos;
    var a = 0.5 -
        c((lat2 - lat1) * p) / 2 +
        c(lat1 * p) * c(lat2 * p) * (1 - c((lon2 - lon1) * p)) / 2;
    return 12742 * asin(sqrt(a));
  }

  void _onStationTap(LatLng stationLocation) {
    LatLng southwest;
    LatLng northeast;

    if (_currentPositon!.latitude < stationLocation.latitude) {
      southwest = _currentPositon!;
      northeast = stationLocation;
    } else {
      southwest = stationLocation;
      northeast = _currentPositon!;
    }

    LatLngBounds bounds =
        LatLngBounds(southwest: southwest, northeast: northeast);

    CameraUpdate cameraUpdate = CameraUpdate.newLatLngBounds(bounds, 150);

    mapController.animateCamera(cameraUpdate);
  }

  Future<List<ParkingStation>> readDatabase() async {
    FirebaseApp secondaryApp = Firebase.app('potent-result-406711');
    final rtdb = FirebaseDatabase.instanceFor(
        app: secondaryApp,
        databaseURL:
            'https://potent-result-406711-ebf47.asia-southeast1.firebasedatabase.app/');

    DatabaseEvent event = await rtdb.ref('parklot_available').once();
    DataSnapshot snapshot = event.snapshot;
    Map<dynamic, dynamic> values = snapshot.value as Map<dynamic, dynamic>;
    var lockey = values.keys;
    for (var loc in lockey) {
      try {
        ParkingStation $loc = ParkingStation(
            stationName: values[loc]['name'],
            availableLots: (values[loc][formattedDateTime()])['current_space'],
            location: LatLng(double.parse(values[loc]['LatLng']['Lat']),
                double.parse(values[loc]['LatLng']['Lng'])),
            distance: (calculateDistance(
                double.parse(values[loc]['LatLng']['Lat']),
                double.parse(values[loc]['LatLng']['Lng']),
                _currentPositon?.latitude ?? 0.0,
                _currentPositon?.longitude ?? 0.0)),
            pricing: values[loc]['Money'],
            onTap:
                _onStationTap); //values[loc]['LatLng']['Lat'], values[loc]['LatLng']['Lng']
        parkingStations.add($loc);
      } catch (e) {
        print('Err: ${values[loc]}-->$e');
      }
    }
    parkingStations.sort((a, b) => a.distance.compareTo(b.distance));
    _completer.complete(parkingStations);
    return parkingStations;
  }

  void _onMapCreated(GoogleMapController controller) {
    mapController = controller;
    if (_mapStyle != null) {
      controller.setMapStyle(_mapStyle);
    } else {
      debugPrint('Failed to load map style');
    }
  }

  @override
  Widget build(BuildContext context) {
//    print(formattedDateTime());
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        extendBodyBehindAppBar: true,
        appBar: _showAppBar
            ? PreferredSize(
                preferredSize: const Size.fromHeight(50.0),
                child: SafeArea(
                  child: Container(
                    margin: const EdgeInsets.symmetric(horizontal: 25.0),
                    decoration: BoxDecoration(
                      color: Colors.blueGrey[100],
                      borderRadius: BorderRadius.circular(30.0),
                    ),
                    child: AppBar(
                      backgroundColor: Colors.transparent,
                      elevation: 0,
                      centerTitle: true,
                      title: const Text(
                        'Charsiu Parking',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 20.0,
                          fontWeight: FontWeight.w400,
                          letterSpacing: 3.0,
                        ),
                      ),
                    ),
                  ),
                ),
              )
            : null,
        body: Stack(
          children: <Widget>[
            GoogleMap(
              onMapCreated: _onMapCreated,
              initialCameraPosition: CameraPosition(
                target: _currentPositon ?? _center,
                zoom: 12.5,
              ),
              markers: {
                Marker(
                  markerId: const MarkerId('current_position'),
                  position: _currentPositon ?? _center,
                  icon: BitmapDescriptor.defaultMarker,
                ),
                for (var station in parkingStations.sublist(0, 10))
                  Marker(
                      markerId: MarkerId(station.stationName),
                      position: station.location!,
                      icon: BitmapDescriptor.defaultMarkerWithHue(
                          BitmapDescriptor.hueCyan)),
              },
              myLocationButtonEnabled: false,
              zoomControlsEnabled: true,
              compassEnabled: false,
            ),
            Positioned(
              right: 15,
              bottom: 100,
              child: FloatingActionButton(
                backgroundColor: const Color.fromRGBO(217, 221, 208, 1),
                elevation: 0.0,
                onPressed: () {
                  if (_currentPositon != null) {
                    mapController.animateCamera(
                      CameraUpdate.newCameraPosition(
                        CameraPosition(
                          target: _currentPositon!,
                          zoom: 15.0,
                        ),
                      ),
                    );
                  }
                },
                child: const Icon(Icons.location_searching),
              ),
            ),
            NotificationListener<ScrollUpdateNotification>(
              onNotification: (notification) {
                if (notification.metrics.extentBefore == 0 &&
                    notification.metrics.extentAfter > 50) {
                  setState(() {
                    _showAppBar = true;
                  });
                } else {
                  setState(() {
                    _showAppBar = false;
                  });
                }
                return true;
              },
              child: DraggableScrollableSheet(
                initialChildSize: 0.3,
                minChildSize: 0.1,
                maxChildSize: 1,
                builder:
                    (BuildContext context, ScrollController scrollController) {
                  return Container(
                    decoration: BoxDecoration(
                      color: Colors.blueGrey[100],
                      borderRadius: const BorderRadius.vertical(
                          top: Radius.circular(20.0)),
                    ),
                    child: FutureBuilder(
                      future: _completer.future,
                      builder: (BuildContext context,
                          AsyncSnapshot<List<ParkingStation>> snapshot) {
                        if (snapshot.connectionState ==
                            ConnectionState.waiting) {
                          //print("UPDATING");
                          return const Center(
                              child: CircularProgressIndicator());
                        } else {
                          return Column(
                            children: [
                              Transform(
                                transform:
                                    Matrix4.diagonal3Values(2.0, 1.0, 1.0),
                                alignment: Alignment.center,
                                child: const Icon(Icons.expand_less),
                              ),
                              Expanded(
                                child: ListView.builder(
                                  controller: scrollController,
                                  itemCount: snapshot.data?.length ?? 0,
                                  itemBuilder:
                                      (BuildContext context, int index) {
                                    return snapshot.data![index];
                                  },
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 20.0,
                                    vertical: 20.0,
                                  ),
                                ),
                              ),
                            ],
                          );
                        }
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
        drawer: Drawer(
          backgroundColor: Colors.blueGrey[100],
          child: ListView(
            padding: EdgeInsets.zero,
            children: <Widget>[
              const SizedBox(
                height: 100,
              ),
              ListTile(
                title: const Text('Settings'),
                onTap: () {
                  Navigator.pop(context);
                },
              ),
              ListTile(
                title: const Text('Bug Report'),
                onTap: () {
                  Navigator.pop(context);
                },
              ),
              ListTile(
                title: const Text('About'),
                onTap: () {
                  Navigator.pop(context);
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> getLocationUpdates() async {
    bool serviceEnable;
    PermissionStatus permissionGranted;

    serviceEnable = await locationController.serviceEnabled();

    if (serviceEnable) {
      serviceEnable = await locationController.requestService();
    } else {
      return;
    }

    permissionGranted = await locationController.hasPermission();
    if (permissionGranted == PermissionStatus.denied) {
      permissionGranted = await locationController.requestPermission();
      if (permissionGranted != PermissionStatus.granted) {
        return;
      }
    }

    locationController.onLocationChanged.listen((LocationData currentLocation) {
      if (currentLocation.latitude != null &&
          currentLocation.longitude != null) {
        setState(() {
          _currentPositon =
              LatLng(currentLocation.latitude!, currentLocation.longitude!);
          //_currentPositon =LatLng(22.632820, 120.300487);
        });
      }
      dev.log("current_pos : ${_currentPositon ?? _center}");
    });
  }
}
