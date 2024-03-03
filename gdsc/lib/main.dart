import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:flutter/services.dart';
import 'package:firebase_database/firebase_database.dart';

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
  final LatLng location;
  //final String pricing;

  const ParkingStation({
    super.key,
    required this.stationName,
    required this.availableLots,
    required this.location,
    //required this.pricing
  });

  /*TO DO:
  This is the default widget for the class, auto generated by copilot
  NEED TO MODIFY
  Distance from user's location to the parking station needs to be generated
  The widget must be adapted to the width of device screen*/
  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white,
      child: Stack(
        children: <Widget>[
          ListTile(
            title: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: <Widget>[
                Text(stationName),
                Text('$availableLots Spaces Left'),
              ],
            ),
            subtitle: const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: <Widget>[
                Text('DISTANCE km'),
                Text('MONEY/hr'),
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
  final LatLng _center = const LatLng(22.6239974, 120.2981408);
  List<ParkingStation> parkingStations = [];
  final Completer<List<ParkingStation>> _completer = Completer();

  String? _mapStyle;
  @override
  void initState() {
    super.initState();
    rootBundle.loadString('assets/mapstyle.txt').then((string) {
      _mapStyle = string;
    });
    readDatabase();
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
      try{
          ParkingStation $loc = ParkingStation(
          stationName: values[loc]['name'],
          availableLots: (values[loc][formattedDateTime()])['current_space'],
          location: _center);
          parkingStations.add($loc);
      }catch(e){
        print(e);

      }
      
    }
    _completer.complete(parkingStations);
    return parkingStations;
  }

  void _onMapCreated(GoogleMapController controller) {
    mapController = controller;
    if (_mapStyle != null) {
      controller.setMapStyle(_mapStyle);
    } else {
      print('Failed to load map style');
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
                target: _center,
                zoom: 12.5,
              ),
              //myLocationButtonEnabled: false,
              zoomControlsEnabled: false,
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
                          return ListView.builder(
                            controller: scrollController,
                            itemCount: snapshot.data?.length ?? 0,
                            itemBuilder: (BuildContext context, int index) {
                              return snapshot.data![index];
                            },
                            padding: const EdgeInsets.symmetric(
                              horizontal: 20.0,
                              vertical: 20.0,
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
}
