import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'main.dart' as mc;

final LatLng? selectedLocation = mc.currentPosition;

class SetLocation extends StatefulWidget {
  const SetLocation({super.key});

  @override
  State createState() => _SetLocationState();
}

class _SetLocationState extends State<SetLocation> {
  void _setLocation(LatLng location) {
    setState(() {
      mc.currentPosition = location;
      //print("location_set: $location");
      mc.mode = 1;
      Navigator.push(
          context, MaterialPageRoute(builder: (context) => const mc.MyApp()));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: PreferredSize(
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
                'Set Location',
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
      ),
      body: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: CameraPosition(
              target: selectedLocation ?? const LatLng(22.632820, 120.300487),
              zoom: 11.0,
            ),
            onTap: _setLocation,
          ),
        ],
      ),
    );
  }
}
