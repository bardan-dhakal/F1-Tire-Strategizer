import 'package:f1_analyzer/bloc/lap_detail_bloc.dart';
import 'package:f1_analyzer/model/lap_detail_model.dart';
import 'package:f1_analyzer/widgets/lap_detail_widget.dart';
import 'package:f1_analyzer/widgets/lap_list_widget.dart';
import 'package:flutter/material.dart';

class StartPage extends StatefulWidget {
  const StartPage({super.key});

  @override
  State<StartPage> createState() => _StartPageState();
}

class _StartPageState extends State<StartPage> {
  final LapDetailBloc bloc = LapDetailBloc();
  int selectedIndex = 0;

  void setSelectedIndex(int index) {
    setState(() {
      selectedIndex = index;
    });
  }

  @override
  void initState() {
    super.initState();
    // No need to call fetchLapDetails() anymore - stream handles real-time updates
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // floatingActionButton: Row(
      //   mainAxisAlignment: MainAxisAlignment.end,
      //   children: [
      //     FloatingActionButton(
      //       onPressed: bloc.storeDummyLapDetails,
      //       child: Icon(Icons.delete),
      //     ),
      //     SizedBox(width: 10),
      //     FloatingActionButton(
      //       onPressed: bloc.fetchLapDetails,
      //       child: Icon(Icons.refresh),
      //     ),
      //   ],
      // ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF0A0A0A), Color(0xFF1A1A1A), Color(0xFF0F0F0F)],
          ),
        ),
        child: Column(
          children: [
            AppBar(
              backgroundColor: Colors.transparent,
              animateColor: false,
              surfaceTintColor: Colors.transparent,
              elevation: 0,
              centerTitle: true,
              title: Text(
                'PitPundits',
                style: Theme.of(
                  context,
                ).textTheme.titleLarge?.copyWith(color: Colors.white),
              ),
            ),
            Expanded(
              child: StreamBuilder<List<TyreModel>>(
                stream: bloc.lapDetailsStream,
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    return Stack(
                      children: [
                        Align(
                          alignment: Alignment.centerLeft,
                          child: SizedBox(
                            width: 200,
                            height: double.infinity,
                            child: LapListWidget(
                              laps: snapshot.data!,
                              onTap: setSelectedIndex,
                              selectedIndex: selectedIndex,
                            ),
                          ),
                        ),
                        Center(
                          child: LapDetailWidget(
                            tyre: snapshot.data![selectedIndex],
                          ),
                        ),
                      ],
                    );
                  } else {
                    return Center(child: LinearProgressIndicator());
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
