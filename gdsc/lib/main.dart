import 'dart:async';
import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:provider/provider.dart';
import 'firebase_options.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:flutter/services.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:location/location.dart' as ploc;
import 'package:google_maps_routes/google_maps_routes.dart' as gmr;
import 'set_location.dart' as sl;
import 'pages.dart' as pages;
import 'key.dart' as key;
//import 'package:flutter/rendering.dart';

const LatLng _center = LatLng(22.6239974, 120.2981408);
final String apikey = Platform.isAndroid
    ? key.Key().androidKey
    : Platform.isIOS
        ? key.Key().iosKey
        : "Unsupport Platform";
gmr.MapsRoutes route = gmr.MapsRoutes();
int mode = 0;
LatLng? currentPosition;

final locationController = ploc.Location();
Stream<ploc.LocationData> locationSubscription =
    locationController.onLocationChanged;
Set<Marker> markerset = {};

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    name: "potent-result-406711",
    options: DefaultFirebaseOptions.currentPlatform,
  );
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
  ));
  if (apikey == "Unsupport Platform") {
    throw Exception("Unsupport Platform");
  }
  runApp(ChangeNotifierProvider(
      create: (context) => pages.ThemeModel(), child: const MyApp()));
}

class ParkingStation extends StatelessWidget {
  final String stationName;
  final int availableLots;
  final LatLng? location;
  final String? pricing;
  final double distance;
  final Function(LatLng, String) onTap;

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
    return Card(
      elevation: 0.0,
      color: Provider.of<pages.ThemeModel>(context).isDarkMode
          ? Colors.grey[800]
          : Colors.white,
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
            onTap:
                location != null ? () => onTap(location!, stationName) : null,
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
    );
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State createState() => _MyAppState();
  // This widget is the root of your application.
}

class _MyAppState extends State {
  late GoogleMapController mapController;
  bool _showAppBar = true;
  List<ParkingStation> parkingStations = [];
  Completer<List<ParkingStation>> parkingStationCompleter = Completer();
  bool drawingroute = false;
  // String? _mapStyle;
  final DraggableScrollableController sheetcontroller =
      DraggableScrollableController();

  @override
  void initState() {
    super.initState();
    initialize();
  }

  Future<void> initialize() async {
    await getLocationUpdates();
    readDatabase();
  }

  void _onStationTap(LatLng stationLocation, String stationName) {
    double southLat = min(currentPosition!.latitude, stationLocation.latitude);
    double northLat = max(currentPosition!.latitude, stationLocation.latitude);

    double westLng = min(currentPosition!.longitude, stationLocation.longitude);
    double eastLng = max(currentPosition!.longitude, stationLocation.longitude);

    LatLng southwest = LatLng(southLat * 0.999999999999, westLng);
    LatLng northeast = LatLng(northLat * 0.999999999999, eastLng);

    LatLngBounds bounds =
        LatLngBounds(southwest: southwest, northeast: northeast);

    CameraUpdate cameraUpdate = CameraUpdate.newLatLngBounds(bounds, 100);

    mapController.animateCamera(cameraUpdate);
    //mapController.showMarkerInfoWindow(MarkerId(stationName));
    sheetcontroller.reset();

    _onMarkerTap(stationLocation, stationName);
  }

  void _onMarkerTap(LatLng targetPos, String name) async {
    setState(() {
      drawingroute = true;
    });
    bool newStation = true;

    route.routes.clear();
    List<LatLng> points = [
      LatLng(currentPosition!.latitude, currentPosition!.longitude),
      LatLng(targetPos.latitude, targetPos.longitude)
    ];
    for (var station in parkingStations.sublist(0, 5)) {
      if (station.location == targetPos) {
        newStation = false;
      }
    }
    if (newStation) {
      refreshMarkers();
      markerset.add(Marker(
        markerId: MarkerId(name),
        position: targetPos,
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueCyan),
        infoWindow: InfoWindow(
          title: name,
        ),
        onTap: () => _onMarkerTap(targetPos, name),
        //anchor: const Offset(0.5, 0) //center of the marker
      ));
    }
    await route.drawRoute(
        points, name, const Color.fromRGBO(130, 78, 210, 1.0), apikey,
        travelMode: gmr.TravelModes.driving);
    setState(() {
      drawingroute = false;
    });
  }

  String formattedDateTime() {
    DateTime now = DateTime.now().subtract(const Duration(minutes: 2));
    int dayOfWeek = now.weekday;
    int timeInMinutes = now.hour * 60 + now.minute;
    int choppedTime = (timeInMinutes * 48) ~/ (24 * 60);
    String formattedDateTime = '$dayOfWeek-$choppedTime';
    return formattedDateTime;
  }

  Future<List<ParkingStation>> readDatabase() async {
    FirebaseApp secondaryApp = Firebase.app('potent-result-406711');
    final rtdb = FirebaseDatabase.instanceFor(
        app: secondaryApp,
        databaseURL:
            'https://potent-result-406711-ebf47.asia-southeast1.firebasedatabase.app/');
    DatabaseEvent event = await rtdb.ref('PA').once();
    DataSnapshot snapshot = event.snapshot;
    Map<dynamic, dynamic> values = snapshot.value as Map<dynamic, dynamic>;
    var lockey = values.keys;
    for (var loc in lockey) {
      try {
        ParkingStation $loc = ParkingStation(
            stationName: values[loc]['N'],
            availableLots: (values[loc][formattedDateTime()])['CS'],
            location: LatLng(double.parse(values[loc]['LL']['Lat']),
                double.parse(values[loc]['LL']['Lng'])),
            distance: (calculateDistance(
                double.parse(values[loc]['LL']['Lat']),
                double.parse(values[loc]['LL']['Lng']),
                currentPosition?.latitude,
                currentPosition?.longitude)),
            pricing: values[loc]['M'],
            onTap: _onStationTap);
        parkingStations.add($loc);
      } catch (e) {
        //print('Err: ${values[loc]}-->$e');
      }
    }
    parkingStations.sort((a, b) => a.distance.compareTo(b.distance));
    parkingStationCompleter.complete(parkingStations);
    parkingStationCompleter.future.then((value) {
      refreshMarkers();
    });
    return parkingStations;
  }

  void refreshMarkers() {
    // 更新你的標記集合
    Set<Marker> newmarker = {};
    markerset.clear();
    newmarker.add(Marker(
      markerId: const MarkerId('current_position'),
      position: currentPosition ?? _center,
      icon: BitmapDescriptor.defaultMarker,
    ));

    for (var station in (parkingStations.length >= 5
        ? parkingStations.sublist(0, 5)
        : parkingStations)) {
      newmarker.add(Marker(
        markerId: MarkerId(station.stationName),
        position: station.location!,
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueCyan),
        infoWindow: InfoWindow(
          title: station.stationName,
        ),
        onTap: () => _onMarkerTap(station.location!, station.stationName),
        //anchor: const Offset(0.5, 0)
      ));
    }
    //print("Marker refreshed!");
    // 通過 setState 觸發 UI 的重繪
    setState(() {
      markerset = newmarker;
    });
  }

  Future<void> refresh() async {
    setState(() {
      parkingStations.clear();
      readDatabase();
    });
    parkingStationCompleter = Completer();
    await Future.delayed(const Duration(seconds: 3));
    refreshMarkers();
    mapController.animateCamera(
      CameraUpdate.newCameraPosition(
        CameraPosition(
          target: currentPosition!,
          zoom: 13.0,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    //print(formattedDateTime())
    final themeModel = Provider.of<pages.ThemeModel>(context);
    return MaterialApp(
        theme: ThemeData.light().copyWith(
            primaryColor: Colors.blueGrey[100],
            floatingActionButtonTheme: FloatingActionButtonThemeData(
                backgroundColor: Colors.blueGrey[200],
                foregroundColor: Colors.black),
            progressIndicatorTheme:
                ProgressIndicatorThemeData(color: Colors.blueGrey[600])),
        darkTheme: ThemeData.dark().copyWith(
            primaryColor: Colors.blueGrey[800],
            floatingActionButtonTheme: FloatingActionButtonThemeData(
                backgroundColor: Colors.blueGrey[600],
                foregroundColor: Colors.white),
            progressIndicatorTheme:
                ProgressIndicatorThemeData(color: Colors.blueGrey[200])),
        themeMode: themeModel.isDarkMode ? ThemeMode.dark : ThemeMode.light,
        debugShowCheckedModeBanner: false,
        home: Builder(
          builder: (context) => Scaffold(
            extendBodyBehindAppBar: true,
            appBar: _showAppBar
                ? PreferredSize(
                    preferredSize: const Size.fromHeight(50.0),
                    child: SafeArea(
                      child: Container(
                        margin: const EdgeInsets.symmetric(horizontal: 25.0),
                        decoration: BoxDecoration(
                          color: Theme.of(context).primaryColor,
                          borderRadius: BorderRadius.circular(30.0),
                        ),
                        child: AppBar(
                          backgroundColor: Colors.transparent,
                          elevation: 0,
                          centerTitle: true,
                          title: const Text(
                            'Charsiu Parking',
                            style: TextStyle(
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
                  key: ValueKey(themeModel.isDarkMode),
                  cloudMapId: (() {
                    final themeModel = Provider.of<pages.ThemeModel>(context);
                    if (Platform.isAndroid) {
                      return themeModel.isDarkMode
                          ? 'e5ab4c2bb5bd724c287afbad' // Android dark mode MapID
                          : 'e5ab4c2bb5bd724ce7ff84e8'; // Android light mode MapID
                    } else if (Platform.isIOS) {
                      return themeModel.isDarkMode
                          ? 'e5ab4c2bb5bd724c8cd48e59' // iOS dark mode MapID
                          : 'e5ab4c2bb5bd724cabef6f84'; // iOS light mode MapID
                    } else {
                      return '';
                    }
                  })(),
                  onMapCreated: (GoogleMapController controller) {
                    mapController = controller;
                  },
                  initialCameraPosition: CameraPosition(
                    target: currentPosition ?? _center,
                    zoom: 12.5,
                  ),
                  markers: markerset,
                  polylines: route.routes,
                  myLocationButtonEnabled: false,
                  zoomControlsEnabled: false,
                  compassEnabled: false,
                ),
                if (drawingroute)
                  const Center(
                    child: CircularProgressIndicator(),
                  ),
                Positioned(
                  right: 15,
                  bottom: 100,
                  child: FloatingActionButton(
                    heroTag: 'locate',
                    elevation: 0.0,
                    onPressed: () {
                      if (currentPosition != null) {
                        mapController.animateCamera(
                          CameraUpdate.newCameraPosition(
                            CameraPosition(
                              target: currentPosition!,
                              zoom: 15.0,
                            ),
                          ),
                        );
                      }
                    },
                    child: const Icon(Icons.location_searching),
                  ),
                ),
                Positioned(
                  right: 15,
                  bottom: 160,
                  child: FloatingActionButton(
                    heroTag: 'refresh',
                    elevation: 0.0,
                    onPressed: () {
                      refresh();
                    },
                    child: const Icon(Icons.refresh),
                  ),
                ),
                NotificationListener<ScrollUpdateNotification>(
                  onNotification: (notification) {
                    if (notification.metrics.extentBefore == 0) {
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
                    controller: sheetcontroller,
                    initialChildSize: 0.1,
                    minChildSize: 0.1,
                    maxChildSize: 1,
                    builder: (BuildContext context,
                        ScrollController sheetcontroller) {
                      return Container(
                        decoration: BoxDecoration(
                          color: Theme.of(context).primaryColor,
                          borderRadius: const BorderRadius.vertical(
                              top: Radius.circular(20.0)),
                        ),
                        child: FutureBuilder(
                          future: parkingStationCompleter.future,
                          builder: (BuildContext context,
                              AsyncSnapshot<List<ParkingStation>> snapshot) {
                            if (snapshot.connectionState ==
                                ConnectionState.waiting) {
                              //print("UPDATING");
                              return const Center(
                                child: CircularProgressIndicator(),
                              );
                            } else {
                              return ListView.builder(
                                controller: sheetcontroller,
                                itemCount: (snapshot.data?.length ?? 0),
                                itemBuilder: (BuildContext context, int index) {
                                  return snapshot.data![index];
                                },
                                padding: const EdgeInsets.only(
                                  top: 30.0,
                                  left: 20.0,
                                  right: 20.0,
                                  bottom: 20.0,
                                ),
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
              backgroundColor: Theme.of(context).primaryColor,
              child: Builder(
                builder: (context) => ListView(
                  padding: EdgeInsets.zero,
                  children: <Widget>[
                    const SizedBox(
                      height: 100,
                    ),
                    ListTile(
                        title: mode == 0
                            ? const Text('Set currrent location')
                            : const Text("Use GPS location"),
                        onTap: () {
                          mode == 0
                              ? {
                                  mode = 1,
                                  Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                          builder: (context) =>
                                              const sl.SetLocation())),
                                  locationController.onLocationChanged
                                      .listen((event) {})
                                      .cancel(),
                                  route.routes.clear(),
                                  refreshMarkers(),
                                  refresh(),
                                }
                              : {
                                  route.routes.clear(),
                                  mode = 0,
                                  Navigator.popUntil(
                                      context, ModalRoute.withName('/')),
                                  getLocationUpdates(),
                                  refresh(),
                                };
                        }),
                    ListTile(
                      title: const Text('Settings'),
                      onTap: () {
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) =>
                                    const pages.SettingsPage()));
                      },
                    ),
                    ListTile(
                      title: const Text('Bug Report'),
                      onTap: () {
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const pages.BugPage()));
                      },
                    ),
                    ListTile(
                      title: const Text('About'),
                      onTap: () {
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const pages.AboutPage()));
                      },
                    ),
                  ],
                ),
              ),
            ),
          ),
        ));
  }

  Future<void> getLocationUpdates() async {
    bool serviceEnable;
    ploc.PermissionStatus permissionGranted;

    serviceEnable = await locationController.serviceEnabled();

    if (serviceEnable) {
      serviceEnable = await locationController.requestService();
    } else {
      return;
    }

    permissionGranted = await locationController.hasPermission();
    if (permissionGranted == ploc.PermissionStatus.denied) {
      permissionGranted = await locationController.requestPermission();
      if (permissionGranted != ploc.PermissionStatus.granted) {
        return;
      }
    }

    locationSubscription.listen((ploc.LocationData currentLocation) {
      if (currentLocation.latitude != null &&
          currentLocation.longitude != null &&
          mode == 0) {
        setState(() {
          currentPosition =
              LatLng(currentLocation.latitude!, currentLocation.longitude!);
        });
      }
      //print("Loc :${currentPosition!},mode=$mode");
    });
  }
}

double calculateDistance(lat1, lon1, lat2, lon2) {
  var p = 0.017453292519943295;
  var c = cos;
  var a = 0.5 -
      c((lat2 - lat1) * p) / 2 +
      c(lat1 * p) * c(lat2 * p) * (1 - c((lon2 - lon1) * p)) / 2;
  return 12742 * asin(sqrt(a));
}
