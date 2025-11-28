import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:f1_analyzer/model/lap_detail_model.dart';

class LapDetailBloc {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  late final Stream<List<TyreModel>> _lapDetailsStream;

  LapDetailBloc() {
    _lapDetailsStream = _firestore
        .collection('laps')
        .orderBy('lap_number', descending: true)
        .snapshots()
        .map((snapshot) {
          final List<TyreModel> lapDetails = [];
          for (var doc in snapshot.docs) {
            final data = doc.data();
            final tyreModel = _convertFirestoreToTyreModel(data);
            if (tyreModel != null) {
              lapDetails.add(tyreModel);
            }
          }
          return lapDetails;
        });
  }

  Stream<List<TyreModel>> get lapDetailsStream => _lapDetailsStream;

  TyreModel? _convertFirestoreToTyreModel(Map<String, dynamic> data) {
    try {
      // Convert compound string to enum
      final compoundString = data['compound'] as String?;
      TyreCompound compound;
      switch (compoundString?.toLowerCase()) {
        case 'soft':
          compound = TyreCompound.soft;
          break;
        case 'medium':
          compound = TyreCompound.medium;
          break;
        case 'hard':
          compound = TyreCompound.hard;
          break;
        case 'intermediate':
          compound = TyreCompound.intermediate;
          break;
        case 'wet':
          compound = TyreCompound.wet;
          break;
        default:
          // Default to hard if compound cannot be determined
          compound = TyreCompound.hard;
          print('Unknown compound: $compoundString, defaulting to hard');
      }

      // Convert color string to enum
      final colorString = data['color'] as String?;

      TyreColor color;
      switch (colorString?.toLowerCase()) {
        case 'matte black':
          color = TyreColor.matteBlack;
          break;
        case 'glossy black':
          color = TyreColor.glossyBlack;
          break;
        case 'purple tin':
          color = TyreColor.purpleTin;
          break;
        case 'grey-black':
          color = TyreColor.greyBlack;
          break;
        case 'pale grey':
          color = TyreColor.paleGrey;
          break;
        default:
          // Default to matte black as per guidelines
          color = TyreColor.matteBlack;
          print('Unknown color: $colorString, defaulting to matte black');
      }

      // Convert wear pattern string to enum
      final wearPatternString = data['wear_pattern'] as String?;

      WearPattern wearPattern;
      switch (wearPatternString?.toLowerCase()) {
        case 'uneven':
          wearPattern = WearPattern.uneven;
          break;
        case 'inner':
          wearPattern = WearPattern.inner;
          break;
        case 'outer':
          wearPattern = WearPattern.outer;
          break;
        case 'center':
          wearPattern = WearPattern.center;
          break;
        case 'even':
          wearPattern = WearPattern.even;
          break;
        default:
          // Default to even as per guidelines
          wearPattern = WearPattern.even;
          print('Unknown wear pattern: $wearPatternString, defaulting to even');
      }

      // Create a single TyreDetailModel with the same values for all tyres
      final tyreDetail = TyreDetailModel(
        color: color,
        wearPattern: wearPattern,
        sidewallDefomation: data['sidewall_deformation'] as bool? ?? false,
        isGraining: data['is_graining'] as bool? ?? false,
        tyrePressure: (data['tyre_pressure'] as num?)?.toInt() ?? 0,
        tyreTemperature: (data['tyre_temperature'] as num?)?.toInt() ?? 0,
      );

      return TyreModel(
        strategy: data['strategy'] as String? ?? '',
        track: data['track'] as String? ?? '',
        trackKnowledge: data['track_strategy'] as String? ?? '',
        lapNumber: (data['lap_number'] as num?)?.toInt() ?? 0,
        compound: compound,
        trackTemperature: (data['track_temperature'] as num?)?.toInt() ?? 0,
        frontLeft: tyreDetail,
        frontRight: tyreDetail,
        rearLeft: tyreDetail,
        rearRight: tyreDetail,
      );
    } catch (e) {
      print('Error converting Firestore data to TyreModel: $e');
      return null;
    }
  }
}
